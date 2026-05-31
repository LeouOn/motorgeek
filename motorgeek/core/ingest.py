"""Agentic ingestion pipeline — state machine, LLM extraction, gap detection, save."""

import json
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from motorgeek.core.llm import LLMClient
from motorgeek.core.models import (
    IngestSessions,
    Car,
    Performance,
    PowertrainICE,
    CostToOwn,
    Dimensions,
    PerformanceMeasurements,
    ZePerfsIndices,
    CarReviews,
)

# ── valid state transitions ──────────────────────────────────────────────────

TRANSITIONS = {
    "draft": {"processing", "discarded"},
    "processing": {"awaiting_response", "discarded"},
    "awaiting_response": {"awaiting_response", "enriched", "discarded"},
    "enriched": {"saved", "discarded"},
    "saved": set(),
    "discarded": set(),
}


def transition(session_obj: IngestSessions, new_status: str, db: Session) -> None:
    """Validate and apply a state transition."""
    if new_status not in TRANSITIONS.get(session_obj.status, set()):
        raise ValueError(
            f"Invalid transition: {session_obj.status} → {new_status}. "
            f"Allowed: {TRANSITIONS.get(session_obj.status, set())}"
        )
    session_obj.status = new_status
    session_obj.updated_at = datetime.now(timezone.utc)
    db.add(session_obj)
    db.commit()


# ── family inheritance ───────────────────────────────────────────────────────

def get_family_defaults(db: Session, family: str) -> dict:
    """Look up existing cars in a family and return inherited traits.
    
    Returns dict with keys like 'make', 'country', 'body_style', 'drivetrain',
    'engine_layout', 'transmission_type' — the values that all members share.
    Returns empty dict if family not found.
    """
    from motorgeek.core.models import PowertrainICE
    
    cars = db.query(Car).filter(Car.family == family).all()
    if not cars:
        cars = db.query(Car).filter(Car.family.ilike(f"%{family}%")).all()
    if not cars:
        return {}

    inherited = {}

    # Identity fields — take from first car (assumed consistent)
    base = cars[0]
    inherited["family"] = family
    if base.make:
        inherited["make"] = base.make
    if base.country:
        inherited["country"] = base.country
    if base.body_style:
        inherited["body_style"] = base.body_style

    # Powertrain fields — check consistency across variants
    ice_rows = []
    for c in cars:
        ice = db.query(PowertrainICE).filter(PowertrainICE.car_id == c.id).first()
        if ice:
            ice_rows.append(ice)

    if ice_rows:
        drivetrains = set(i.drivetrain for i in ice_rows if i.drivetrain)
        if len(drivetrains) == 1:
            inherited["drivetrain"] = drivetrains.pop()

        layouts = set(i.engine_layout for i in ice_rows if i.engine_layout)
        if len(layouts) == 1:
            inherited["engine_layout"] = layouts.pop()

        transmissions = set(i.transmission_type for i in ice_rows if i.transmission_type)
        if len(transmissions) == 1:
            inherited["transmission_type"] = transmissions.pop()

    # Collect variant names for context
    variants = [c.variant for c in cars if c.variant]
    if variants:
        inherited["sibling_variants"] = variants

    inherited["family_size"] = len(cars)
    return inherited


def build_family_context(inherited: dict) -> str:
    """Build a text block describing family inheritance for the LLM prompt."""
    if not inherited:
        return ""

    lines = [f"\n## Family Context: {inherited.get('family', 'Unknown')}"]
    lines.append(f"This car belongs to the '{inherited['family']}' family ({inherited.get('family_size', 0)} variants already in collection).")

    if inherited.get("sibling_variants"):
        lines.append(f"Existing variants: {', '.join(inherited['sibling_variants'])}")

    lines.append("\nInherited traits (apply unless explicitly overridden by the new variant):")
    for field, label in [
        ("make", "Make"), ("country", "Country"), ("body_style", "Body style"),
        ("drivetrain", "Drivetrain"), ("engine_layout", "Engine layout"),
        ("transmission_type", "Transmission type"),
    ]:
        if field in inherited:
            lines.append(f"  - {label}: {inherited[field]}")

    lines.append("\nOnly extract variant-specific details: engine specs (HP, torque, displacement), performance figures, price, weight. Do NOT change inherited traits unless the text explicitly states otherwise.")
    return "\n".join(lines)


# ── session CRUD ─────────────────────────────────────────────────────────────

def create_session(
    db: Session,
    raw_paste: str,
    source_url: Optional[str] = None,
    source_site: Optional[str] = None,
    car_id: Optional[int] = None,
) -> IngestSessions:
    """Create a new ingest session in draft status."""
    session_obj = IngestSessions(
        car_id=car_id,
        raw_paste=raw_paste,
        source_url=source_url,
        source_site=source_site,
        status="draft",
        agent_messages=[],
    )
    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)
    return session_obj


def get_session_by_id(db: Session, session_id: int) -> Optional[IngestSessions]:
    return db.query(IngestSessions).filter(IngestSessions.id == session_id).first()


def list_sessions(db: Session) -> list[IngestSessions]:
    return db.query(IngestSessions).order_by(IngestSessions.updated_at.desc()).all()


# ── agentic extraction prompt ────────────────────────────────────────────────

AGENTIC_EXTRACTION_PROMPT = """You are an automotive data extraction agent. Analyze the provided text about a car and produce structured JSON.

## Instructions
1. Extract ALL numeric values with their units. Convert to canonical units where possible (hp, Nm, mm, kg, seconds, km/h).
2. For each field, assign a confidence level: "high" (exact match in text), "medium" (inferred from context), "low" (guessed or single uncorroborated source).
3. Identify GAPS — fields you would expect for a car spec but that are missing from the text.
4. Identify CONFLICTS — values that contradict each other (e.g. manufacturer claim 5.5s 0-60 but measured 5.7s).
5. Generate QUESTIONS for the user — things you need clarified to proceed.
6. If a car identity (make, model, generation, year) can be inferred from the text, include it.

## Output format — return ONLY valid JSON, no markdown:

{
  "identity": {
    "make": "Genesis",
    "model": "G90",
    "generation": "first",
    "year_start": 2016,
    "year_end": 2022,
    "body_style": "sedan",
    "country": "South Korea",
    "era_tag": "modern"
  },
  "dimensions": {
    "length_mm": {"value": 5205, "confidence": "high"},
    "width_mm": {"value": 1915, "confidence": "high"},
    "height_mm": {"value": 1495, "confidence": "high"},
    "wheelbase_mm": {"value": 3160, "confidence": "high"},
    "track_front_mm": {"value": 1640, "confidence": "high"},
    "track_rear_mm": {"value": 1639, "confidence": "high"},
    "ground_clearance_mm": {"value": 130, "confidence": "high"}
  },
  "powertrain": {
    "engine_layout": {"value": "front longitudinal", "confidence": "high"},
    "displacement_cc": {"value": 3342, "confidence": "high"},
    "cylinders": {"value": 6, "confidence": "high"},
    "aspiration": {"value": "twin-turbo", "confidence": "high"},
    "horsepower_bhp": {"value": 370, "confidence": "high"},
    "horsepower_rpm": {"value": 6000, "confidence": "high"},
    "torque_nm": {"value": 510, "confidence": "high"},
    "torque_rpm": {"value": 1300, "confidence": "medium"},
    "fuel_system": {"value": "direct injection", "confidence": "high"},
    "transmission_type": {"value": "automatic", "confidence": "high"},
    "gear_count": {"value": 8, "confidence": "high"},
    "drivetrain": {"value": "AWD", "confidence": "high"},
    "curb_weight_kg": {"value": 2170, "confidence": "high"},
    "weight_dist_pct": {"value": "53/47", "confidence": "high"},
    "fuel_consumption_mixed_l_100km": {"value": 9.8, "confidence": "high"},
    "fuel_consumption_sport_l_100km": {"value": 13.9, "confidence": "high"},
    "fuel_tank_capacity_l": {"value": 83, "confidence": "high"},
    "power_kw": {"value": 272, "confidence": "high"},
    "top_speed_claimed_kmh": {"value": null, "confidence": "low"}
  },
  "performance": {
    "measurements": [
      {"metric_name": "accel_0_100", "value": 5.7, "unit": "s", "source_site": "ZePerfs", "sample_size": 3, "confidence": "high"},
      {"metric_name": "accel_0_160", "value": 13.8, "unit": "s", "source_site": "ZePerfs", "sample_size": 3, "confidence": "medium"},
      {"metric_name": "quarter_mile_time", "value": 13.9, "unit": "s", "source_site": "ZePerfs", "sample_size": 2, "confidence": "high"},
      {"metric_name": "quarter_mile_speed", "value": 162, "unit": "km/h", "source_site": "ZePerfs", "sample_size": 2, "confidence": "high"},
      {"metric_name": "brake_100_0", "value": 39.0, "unit": "m", "source_site": "ZePerfs", "sample_size": 2, "confidence": "high"},
      {"metric_name": "top_speed_measured", "value": 281, "unit": "km/h", "source_site": "ZePerfs", "sample_size": 1, "confidence": "medium"}
    ]
  },
  "indices": {
    "zeperfs_index": {"value": 154, "confidence": "high"},
    "sportivity_index": {"value": 103, "confidence": "high"},
    "perfs_prix_ratio": {"value": 90, "confidence": "high"}
  },
  "market": {
    "msrp_original": {"value": 94400, "confidence": "medium"},
    "msrp_currency": {"value": "EUR", "confidence": "medium"}
  },
  "reviews": [
    {"source_site": "ZePerfs", "rating_overall": 4.1, "confidence": "high"},
    {"source_site": "KBB", "rating_overall": 4.8, "confidence": "high"}
  ],
  "gaps": [
    "No top speed from manufacturer (only estimated 281 km/h from ZePerfs)",
    "No CO2 emissions data",
    "No drag coefficient",
    "No lateral G or skidpad figures",
    "No Nürburgring or other circuit lap times"
  ],
  "conflicts": [
    {"field": "curb_weight_kg", "values": [2170, 2245, 2263], "sources": ["DIN", "UE", "UE measured"], "note": "DIN vs EU curb weight standards differ. Measured weight 2263 kg with driver."}
  ],
  "questions": [
    "What is the fuel type — petrol or diesel? (I assume petrol based on HP/displacement ratio)",
    "Should I store curb weight as 2170 kg (DIN), 2245 kg (EU), or 2263 kg (measured running weight)?",
    "The car has two engine options (3.3T V6 and 5.0 V8). Which one is this data for?",
    "Do you have any reliability data (common failures, repair costs) you can share?"
  ]
}

Text to analyze:
{text}"""


# ── pipeline execution ───────────────────────────────────────────────────────

def process_session(
    db: Session,
    session_id: int,
    family: Optional[str] = None,
) -> IngestSessions:
    """Run the full agentic extraction pipeline on a draft session.
    
    If family is provided, inheritance context is injected into the prompt
    so the LLM knows shared traits and only extracts variant-specific details.
    """
    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        raise ValueError(f"Session {session_id} not found")
    if session_obj.status != "draft":
        raise ValueError(f"Session must be in draft status, got {session_obj.status}")

    transition(session_obj, "processing", db)

    # Build inheritance context if family is known
    family_context = ""
    if family:
        inherited = get_family_defaults(db, family)
        if inherited:
            family_context = build_family_context(inherited)
            # Store the family on the session
            session_obj.source_site = (session_obj.source_site or "") + f" [family: {family}]"

    llm = LLMClient()

    # Build the prompt — inject family context before the text
    raw_text = session_obj.raw_paste
    if family_context:
        raw_text = family_context + "\n\n---\n\n" + raw_text
    prompt = AGENTIC_EXTRACTION_PROMPT.replace("{text}", raw_text)

    try:
        raw_response = llm.complete(prompt)

        # Parse the JSON from the response
        parsed = _parse_llm_json(raw_response)

        session_obj.parsed_data = parsed
        session_obj.llm_model = llm.model

        # Extract gaps and questions into dedicated fields
        session_obj.gaps_and_questions = {
            "gaps": parsed.get("gaps", []),
            "conflicts": parsed.get("conflicts", []),
            "questions": parsed.get("questions", []),
        }

        # Build agent welcome message
        gaps_count = len(parsed.get("gaps", []))
        questions_count = len(parsed.get("questions", []))
        conflicts_count = len(parsed.get("conflicts", []))

        intro = (
            f"I've analyzed your paste and extracted structured data. "
            f"I found {gaps_count} gap(s), {conflicts_count} conflict(s), "
            f"and have {questions_count} question(s) for you. "
            f"Review the parsed data on the left and answer my questions below."
        )

        session_obj.agent_messages = [
            {"role": "agent", "text": intro, "timestamp": datetime.now(timezone.utc).isoformat()}
        ]

        transition(session_obj, "awaiting_response", db)
        db.refresh(session_obj)
        return session_obj

    except Exception as e:
        session_obj.agent_messages = [
            {"role": "agent", "text": f"Processing failed: {e}", "timestamp": datetime.now(timezone.utc).isoformat()}
        ]
        db.add(session_obj)
        db.commit()
        raise


def respond_to_session(db: Session, session_id: int, user_message: str) -> IngestSessions:
    """User sends a message/answer to the agent. Agent processes and updates parsed data."""
    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        raise ValueError(f"Session {session_id} not found")
    if session_obj.status not in ("awaiting_response", "enriched"):
        raise ValueError(f"Session must be in awaiting_response or enriched, got {session_obj.status}")

    # Append user message
    messages = session_obj.agent_messages or []
    messages.append({"role": "user", "text": user_message, "timestamp": datetime.now(timezone.utc).isoformat()})

    # Ask LLM to incorporate the user's response
    llm = LLMClient()
    followup_prompt = _build_followup_prompt(
        parsed_data=session_obj.parsed_data or {},
        gaps_and_questions=session_obj.gaps_and_questions or {},
        user_message=user_message,
    )

    try:
        raw_response = llm.complete(followup_prompt)
        updated = _parse_llm_json(raw_response)

        # Merge updates into parsed_data (but NOT questions — those we replace)
        if session_obj.parsed_data:
            updated_without_questions = {k: v for k, v in updated.items() if k != "questions"}
            _deep_merge(session_obj.parsed_data, updated_without_questions)

        # Explicitly REPLACE questions (don't merge — answered questions should be removed)
        remaining_questions = updated.get("questions", [])
        # Sync questions to both storage locations
        session_obj.gaps_and_questions = {
            **(session_obj.gaps_and_questions or {}),
            "questions": remaining_questions,
        }
        if session_obj.parsed_data:
            session_obj.parsed_data["questions"] = remaining_questions
        if not remaining_questions:
            # All questions answered — move to enriched
            agent_reply = "Thanks! I've incorporated your answers. The data looks complete. Click 'Looks Good, Save' when ready."
            session_obj.status = "enriched"
        else:
            agent_reply = (
                f"I've updated the data based on your response. "
                f"I still have {len(remaining_questions)} question(s):\n"
                + "\n".join(f"• {q}" for q in remaining_questions)
            )

        messages.append({"role": "agent", "text": agent_reply, "timestamp": datetime.now(timezone.utc).isoformat()})
        session_obj.agent_messages = messages
        session_obj.updated_at = datetime.now(timezone.utc)
        db.add(session_obj)
        db.commit()
        db.refresh(session_obj)
        return session_obj

    except Exception as e:
        messages.append({"role": "agent", "text": f"Error processing your response: {e}", "timestamp": datetime.now(timezone.utc).isoformat()})
        session_obj.agent_messages = messages
        db.add(session_obj)
        db.commit()
        raise


def save_session(db: Session, session_id: int) -> int:
    """Save the enriched data to the DB. Returns car_id."""
    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        raise ValueError(f"Session {session_id} not found")
    if session_obj.status not in ("enriched",):
        raise ValueError(f"Session must be in enriched status, got {session_obj.status}")

    parsed = session_obj.parsed_data or {}
    identity = parsed.get("identity", {})

    # Create or update Car
    if session_obj.car_id:
        car = db.query(Car).filter(Car.id == session_obj.car_id).first()
    else:
        car = Car()

    _apply_identity(car, identity)
    db.add(car)
    db.flush()  # get car.id

    car_id = car.id
    session_obj.car_id = car_id

    # Dimensions
    dims = parsed.get("dimensions", {})
    if dims:
        _upsert_dimensions(db, car_id, dims)

    # Powertrain
    pt = parsed.get("powertrain", {})
    if pt:
        _upsert_powertrain(db, car_id, pt)

    # Performance measurements
    perf = parsed.get("performance", {})
    measurements = perf.get("measurements", []) if isinstance(perf, dict) else []
    if measurements:
        _upsert_performance_measurements(db, car_id, measurements)

    # Also try to populate aggregate Performance row from measurements
    _populate_performance_aggregate(db, car_id, measurements)

    # ZePerfs indices
    indices = parsed.get("indices", {})
    if indices:
        _upsert_zeperfs_indices(db, car_id, indices)

    # Market
    market = parsed.get("market", {})
    if market:
        _upsert_cost_to_own(db, car_id, market)

    # Reviews
    reviews = parsed.get("reviews", [])
    if reviews:
        _upsert_reviews(db, car_id, reviews)

    transition(session_obj, "saved", db)
    db.refresh(session_obj)
    return car_id


# ── helpers ──────────────────────────────────────────────────────────────────


def _parse_llm_json(text: str) -> dict:
    """Extract a JSON object from LLM output, stripping markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        # Remove opening fence
        idx = text.find("\n")
        if idx != -1:
            text = text[idx + 1:]
        else:
            text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    return json.loads(text)


def _build_followup_prompt(
    parsed_data: dict,
    gaps_and_questions: dict,
    user_message: str,
) -> str:
    remaining = gaps_and_questions.get("questions", [])
    if remaining:
        questions_block = "\n".join(f"{i+1}. {q}" for i, q in enumerate(remaining))
        questions_instruction = (
            f"## Questions to resolve (the user is answering these now):\n{questions_block}\n\n"
            f"IMPORTANT: The user's response below addresses these {len(remaining)} questions. "
            f"Your response MUST have \"questions\": [] unless the user's answer reveals a completely new gap "
            f"that wasn't in the list above. Do NOT re-ask questions from this list."
        )
    else:
        questions_instruction = ""

    return f"""You are an automotive data extraction agent. The user is answering your questions.

## Current parsed data:
{json.dumps(parsed_data, indent=2, default=str)}

{questions_instruction}

Current gaps: {json.dumps(gaps_and_questions.get('gaps', []))}
Current conflicts: {json.dumps(gaps_and_questions.get('conflicts', []))}

## User's response:
{user_message}

## Instructions:
1. Update parsed_data with any corrections or new values from the user's response.
2. Return ONLY a JSON object. Include ONLY the sections that changed (don't repeat unchanged data).
3. The "questions" field MUST be [] unless the user revealed a genuinely new missing piece of data.

Return ONLY: {{"identity": {{...}}, "dimensions": {{...}}, "powertrain": {{...}}, "performance": {{...}}, "indices": {{...}}, "market": {{...}}, "reviews": [...], "gaps": [...], "conflicts": [...], "questions": [...]}}"""


def _deep_merge(base: dict, overlay: dict) -> None:
    """Merge overlay into base in-place."""
    for key, value in overlay.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        elif key in base and isinstance(base[key], list) and isinstance(value, list):
            base[key].extend(value)
        else:
            base[key] = value


def _apply_identity(car: Car, identity: dict) -> None:
    """Apply identity fields to a Car object."""
    for field in ("make", "model", "generation", "body_style", "country", "era_tag", "description"):
        if field in identity and identity[field]:
            val = identity[field]
            if isinstance(val, dict):
                val = val.get("value", val)
            setattr(car, field, val)
    # Ensure required fields have defaults
    if not car.generation:
        car.generation = ""
    if not car.make:
        car.make = "Unknown"
    if not car.model:
        car.model = "Unknown"
    if car.year_start is None:
        car.year_start = 0
    for field in ("year_start", "year_end", "production_units"):
        if field in identity and identity[field] is not None:
            val = identity[field]
            if isinstance(val, dict):
                val = val.get("value", val)
            setattr(car, field, val)


def _extract_value(field_data) -> Optional[float]:
    """Extract a scalar value from a field that might be {value, confidence} or raw."""
    if field_data is None:
        return None
    if isinstance(field_data, dict):
        return field_data.get("value")
    return field_data


def _extract_str(field_data) -> Optional[str]:
    if field_data is None:
        return None
    if isinstance(field_data, dict):
        val = field_data.get("value")
        return str(val) if val is not None else None
    return str(field_data)


def _upsert_dimensions(db: Session, car_id: int, dims: dict) -> None:
    existing = db.query(Dimensions).filter(Dimensions.car_id == car_id).first()
    if not existing:
        existing = Dimensions(car_id=car_id)
    for field in (
        "length_mm", "width_mm", "height_mm", "wheelbase_mm",
        "track_front_mm", "track_rear_mm", "front_overhang_mm", "rear_overhang_mm",
    ):
        val = _extract_value(dims.get(field))
        if val is not None:
            setattr(existing, field, int(val))
    existing.source = _extract_str(dims.get("source")) or "agentic-ingest"
    db.add(existing)


def _upsert_powertrain(db: Session, car_id: int, pt: dict) -> None:
    existing = db.query(PowertrainICE).filter(PowertrainICE.car_id == car_id).first()
    if not existing:
        existing = PowertrainICE(car_id=car_id)
    scalar_fields = (
        "displacement_cc", "cylinders", "horsepower_bhp", "horsepower_rpm",
        "torque_nm", "torque_rpm", "redline_rpm", "compression_ratio",
        "gear_count", "curb_weight_kg", "drag_coefficient",
        "ground_clearance_mm", "cargo_volume_liters",
        "power_kw", "specific_power_per_cylinder_w_cm2", "bmep_bar",
        "mean_piston_speed_m_s", "engine_torque_nm",
        "fuel_consumption_mixed_l_100km", "fuel_consumption_sport_l_100km",
        "co2_emissions_g_km", "fuel_tank_capacity_l", "reserve_fuel_l",
        "top_speed_claimed_kmh", "power_reserve_pct",
    )
    for field in scalar_fields:
        val = _extract_value(pt.get(field))
        if val is not None:
            setattr(existing, field, float(val) if "weight" in field or "speed" in field or "coefficient" in field or "ratio" in field or "consumption" in field else val)
    str_fields = (
        "engine_layout", "aspiration", "fuel_system", "transmission_type",
        "drivetrain", "weight_dist_pct", "suspension_fr", "brakes_fr",
    )
    for field in str_fields:
        val = _extract_str(pt.get(field))
        if val is not None:
            setattr(existing, field, val)
    existing.source = _extract_str(pt.get("source")) or "agentic-ingest"
    db.add(existing)


def _upsert_performance_measurements(db: Session, car_id: int, measurements: list) -> None:
    for m in measurements:
        if not isinstance(m, dict):
            continue
        metric_name = m.get("metric_name", "")
        value = m.get("value")
        unit = m.get("unit", "")
        source_site = m.get("source_site", "unknown")
        if not metric_name or value is None or not unit:
            continue
        existing = (
            db.query(PerformanceMeasurements)
            .filter(
                PerformanceMeasurements.car_id == car_id,
                PerformanceMeasurements.metric_name == metric_name,
                PerformanceMeasurements.source_site == source_site,
            )
            .first()
        )
        if existing:
            existing.value = float(value)
            existing.unit = unit
            existing.sample_size = m.get("sample_size")
        else:
            pm = PerformanceMeasurements(
                car_id=car_id,
                metric_name=metric_name,
                value=float(value),
                unit=unit,
                source_site=source_site,
                sample_size=m.get("sample_size"),
                conditions=m.get("conditions"),
                notes=m.get("notes"),
            )
            db.add(pm)


def _populate_performance_aggregate(db: Session, car_id: int, measurements: list) -> None:
    """Try to populate the aggregated Performance row from measurement data."""
    existing = db.query(Performance).filter(Performance.car_id == car_id).first()
    if not existing:
        existing = Performance(car_id=car_id, source="agentic-ingest")

    metric_map = {
        "accel_0_60": "accel_0_60",
        "accel_0_100": "accel_0_100",
        "quarter_mile_time": "quarter_mile_time",
        "quarter_mile_speed": "quarter_mile_speed",
        "top_speed_measured": "top_speed_mph",
        "top_speed_claimed": "top_speed_mph",
        "lateral_g": "lateral_g",
    }

    for m in measurements:
        if not isinstance(m, dict):
            continue
        metric_name = m.get("metric_name", "")
        if metric_name in metric_map:
            val = m.get("value")
            if val is not None:
                setattr(existing, metric_map[metric_name], float(val))

    db.add(existing)


def _upsert_zeperfs_indices(db: Session, car_id: int, indices: dict) -> None:
    existing = db.query(ZePerfsIndices).filter(ZePerfsIndices.car_id == car_id).first()
    if not existing:
        existing = ZePerfsIndices(car_id=car_id)
    for field in ("zeperfs_index", "sportivity_index", "perfs_prix_ratio"):
        val = _extract_value(indices.get(field))
        if val is not None:
            setattr(existing, field, float(val))
    existing.source = _extract_str(indices.get("source")) or "agentic-ingest"
    db.add(existing)


def _upsert_cost_to_own(db: Session, car_id: int, market: dict) -> None:
    existing = db.query(CostToOwn).filter(CostToOwn.car_id == car_id).first()
    if not existing:
        existing = CostToOwn(car_id=car_id)
    msrp = _extract_value(market.get("msrp_original"))
    if msrp is not None:
        existing.msrp_original = float(msrp)
    currency = _extract_str(market.get("msrp_currency"))
    if currency:
        existing.msrp_currency = currency
    existing.source = _extract_str(market.get("source")) or "agentic-ingest"
    db.add(existing)


def _upsert_reviews(db: Session, car_id: int, reviews: list) -> None:
    for r in reviews:
        if not isinstance(r, dict):
            continue
        source_site = _extract_str(r.get("source_site"))
        if not source_site:
            continue
        existing = (
            db.query(CarReviews)
            .filter(CarReviews.car_id == car_id, CarReviews.source_site == source_site)
            .first()
        )
        rating = _extract_value(r.get("rating_overall"))
        if not existing:
            existing = CarReviews(car_id=car_id, source_site=source_site)
        if rating is not None:
            existing.rating_overall = float(rating)
        for field in ("rating_reliability", "rating_performance", "rating_comfort", "rating_value"):
            val = _extract_value(r.get(field))
            if val is not None:
                setattr(existing, field, float(val))
        excerpt = _extract_str(r.get("review_excerpt"))
        if excerpt:
            existing.review_excerpt = excerpt
        url = _extract_str(r.get("review_url"))
        if url:
            existing.review_url = url
        db.add(existing)


# ── Batch comparison ingestion ───────────────────────────────────────────────

BATCH_COMPARISON_PROMPT = """You are a car data extraction specialist. Extract ALL cars and qualitative analysis from this multi-car comparison document.

## Instructions
1. Find EVERY car mentioned with specs (MSRP, horsepower, torque, 0-60, weight, platform, engine, drivetrain).
2. For each car, extract: make, model, generation, year_start, year_end, msrp, horsepower, torque_nm, platform, engine_desc, drivetrain, body_style, country.
3. Extract any qualitative analysis: platform comparisons, reliability assessments, cost-of-ownership estimates, recommendations.
4. Identify which cars are being compared against each other.
5. Convert all values to metric where possible (torque to Nm, weight to kg).

## Output format — return ONLY valid JSON:
{
  "cars": [
    {
      "make": "Cadillac",
      "model": "CTS",
      "generation": "3rd gen",
      "year_start": 2015,
      "year_end": 2019,
      "msrp": 45000,
      "horsepower": 265,
      "torque_nm": 400,
      "platform": "GM Alpha II",
      "engine_desc": "2.0L turbo I4",
      "drivetrain": "RWD",
      "body_style": "sedan",
      "country": "USA",
      "variants": [
        {"name": "CTS-V", "horsepower": 640, "msrp": 86000, "engine_desc": "6.2L supercharged V8"}
      ]
    }
  ],
  "qualitative_analysis": {
    "title": "CTS 3rd Gen vs Competitors",
    "platform_comparison": {
      "Alpha II": "Best for aging reliability — simple electronics, no 48V hybrid",
      "CLAR": "Good — B58 engine robust, cooling system aging risk, dense electronics",
      "MLB Evo": "Moderate — 48V failures documented, MMI voltage sensitivity",
      "M3 (Genesis)": "Moderate to below average — reliability trending down"
    },
    "engine_analysis": {
      "B58": "Mechanically robust, 200K+ capable, plastic cooling weak point",
      "M276": "Best Mercedes engine in 20 years, 200K+ service life"
    },
    "cost_estimates": {
      "annual_maintenance": {"CTS": "800-1200", "BMW 5": "1200-1800", "Genesis": "800-1200"}
    },
    "recommendations": [
      {"car": "W212 E350", "price_range": "$15K-22K", "reason": "M276 V6, proven reliability, lowest risk"},
      {"car": "G80 2.5T", "price_range": "$35K-45K", "reason": "Best warranty, lowest running costs"}
    ],
    "key_insight": "Alpha II wins on aging reliability because it was never designed for EV/hybrid — narrow scope becomes an asset at year 10-15."
  },
  "comparison_group": "Luxury Sport Sedans 2015-2025"
}

Text to analyze:
{text}"""


def batch_ingest_comparison(
    db: Session,
    raw_text: str,
    source_url: Optional[str] = None,
    source_site: Optional[str] = None,
) -> dict:
    """Process a multi-car comparison document. Returns summary of what was ingested."""
    from motorgeek.core.models import ComparisonSession, HistoricalContext, LLMAnalyses

    llm = LLMClient()
    prompt = BATCH_COMPARISON_PROMPT.replace("{text}", raw_text)

    try:
        raw_response = llm.complete(prompt)
        parsed = _parse_llm_json(raw_response)
    except Exception as e:
        return {"error": f"LLM extraction failed: {e}", "cars_ingested": 0}

    cars_data = parsed.get("cars", [])
    qualitative = parsed.get("qualitative_analysis", {})
    comparison_name = parsed.get("comparison_group", "Batch Import")

    ingested_cars = []
    car_ids = []

    for car_entry in cars_data:
        try:
            # Create a minimal car entry
            make = car_entry.get("make", "Unknown")
            model = car_entry.get("model", "Unknown")
            gen = car_entry.get("generation", "")

            car = Car(
                make=make,
                model=model,
                generation=gen or "",
                year_start=car_entry.get("year_start") or 0,
                year_end=car_entry.get("year_end"),
                body_style=car_entry.get("body_style", "sedan"),
                country=car_entry.get("country", ""),
                character="luxury" if car_entry.get("msrp", 0) > 40000 else "warm",
                family=model,
                variant=gen or "base",
            )
            db.add(car)
            db.flush()

            # Add powertrain if specs available
            hp = car_entry.get("horsepower")
            torque = car_entry.get("torque_nm")
            if hp or torque:
                ice = PowertrainICE(
                    car_id=car.id,
                    horsepower_bhp=hp,
                    torque_nm=torque,
                    drivetrain=car_entry.get("drivetrain", ""),
                    engine_layout=car_entry.get("engine_desc", ""),
                    source=source_site or "batch-comparison",
                )
                db.add(ice)

            # Add cost data
            msrp = car_entry.get("msrp")
            if msrp:
                cost = CostToOwn(
                    car_id=car.id,
                    msrp_original=float(msrp),
                    msrp_currency="USD",
                    source=source_site or "batch-comparison",
                )
                db.add(cost)

            car_ids.append(car.id)
            ingested_cars.append(f"{make} {model} ({gen})")
            db.commit()

        except Exception as e:
            db.rollback()
            ingested_cars.append(f"FAILED: {car_entry.get('make','?')} {car_entry.get('model','?')} — {e}")

    # Store qualitative analysis as HistoricalContext for the first car (as representative)
    if car_ids and qualitative:
        try:
            # Store platform analysis
            platform_data = qualitative.get("platform_comparison", {})
            engine_data = qualitative.get("engine_analysis", {})
            recommendations = qualitative.get("recommendations", [])
            key_insight = qualitative.get("key_insight", "")

            # Create a comparison session linking all cars
            comp_session = ComparisonSession(
                name=comparison_name,
                car_ids=car_ids,
            )
            db.add(comp_session)

            # Store the full qualitative analysis as an LLM analysis on the first car
            analysis = LLMAnalyses(
                car_id=car_ids[0],
                dimension="comparison",
                model_used=llm.model,
                generated_text=json.dumps(qualitative, indent=2, default=str),
                scores={"cars_analyzed": len(car_ids)},
            )
            db.add(analysis)

            db.commit()
        except Exception:
            db.rollback()

    return {
        "cars_ingested": len(ingested_cars),
        "car_ids": car_ids,
        "cars": ingested_cars,
        "comparison_name": comparison_name,
        "has_qualitative_analysis": bool(qualitative),
        "platform_count": len(qualitative.get("platform_comparison", {})),
        "recommendation_count": len(qualitative.get("recommendations", [])),
    }
