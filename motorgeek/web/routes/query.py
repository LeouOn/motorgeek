# motorgeek/web/routes/query.py
import os
from datetime import datetime, timezone
from fastapi import Request, Form
from fastapi.responses import HTMLResponse

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Performance, PowertrainICE, Reliability, MarketHistory
from motorgeek.core.llm import LLMClient
from motorgeek.web.app import templates


def query_page(request: Request) -> HTMLResponse:
    conversation = request.session.get("conversation", [])
    session = get_session()
    cars = session.query(Car).all()
    return templates.TemplateResponse(request, "query/index.html", {
        "cars": cars, "conversation": conversation,
    })


def query_post(request: Request, message: str = Form(...)) -> HTMLResponse:
    message = message.strip()
    if not message:
        conversation = request.session.get("conversation", [])
        session = get_session()
        cars = session.query(Car).all()
        return templates.TemplateResponse(request, "query/index.html", {
            "cars": cars, "conversation": conversation,
        })

    conversation = request.session.get("conversation", [])
    session = get_session()

    now = datetime.now(timezone.utc).isoformat()
    user_entry = {"role": "user", "text": message, "timestamp": now}
    conversation.append(user_entry)

    agent_text = None
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        agent_text = "LLM not configured. Set OPENAI_API_KEY environment variable."
    else:
        cars = session.query(Car).all()
        car_context = _build_car_context(cars)

        if not cars:
            agent_text = "Your collection is empty. Add some cars first."
        else:
            prompt = _build_prompt(car_context, conversation, message)
            try:
                llm = LLMClient()
                agent_text = llm.complete(prompt)
            except Exception as e:
                agent_text = f"Sorry, I couldn't process that: {e}. Try again."

    if agent_text is None:
        agent_text = "Sorry, I couldn't process that. Try again."

    now = datetime.now(timezone.utc).isoformat()
    conversation.append({"role": "agent", "text": agent_text, "timestamp": now})
    request.session["conversation"] = conversation

    cars = session.query(Car).all()
    return templates.TemplateResponse(request, "query/index.html", {
        "cars": cars, "conversation": conversation,
    })


def query_clear(request: Request) -> HTMLResponse:
    request.session["conversation"] = []
    session = get_session()
    cars = session.query(Car).all()
    return templates.TemplateResponse(request, "query/index.html", {
        "cars": cars, "conversation": [],
    })


def _build_car_context(cars: list[Car]) -> str:
    session = get_session()
    lines = []
    for car in cars:
        year_range = f"{car.year_start or '?'}"
        if car.year_end:
            year_range += f"-{car.year_end}"

        hp = "-"
        accel_60 = "-"
        rel_score = "-"
        price_low = "-"
        price_high = "-"

        ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        if ice and ice.horsepower_bhp:
            hp = f"{ice.horsepower_bhp:.0f}"

        perf = session.query(Performance).filter(Performance.car_id == car.id).first()
        if perf and perf.accel_0_60:
            accel_60 = f"{perf.accel_0_60:.1f}"

        rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
        if rel and rel.reliability_score is not None:
            rel_score = f"{rel.reliability_score:.0f}"

        market = (
            session.query(MarketHistory)
            .filter(MarketHistory.car_id == car.id)
            .order_by(MarketHistory.date_recorded.desc())
            .first()
        )
        if market:
            if market.price_low is not None:
                price_low = f"${market.price_low:,.0f}"
            if market.price_high is not None:
                price_high = f"${market.price_high:,.0f}"

        body = car.body_style or "-"
        country = car.country or "-"
        era = car.era_tag or "-"

        line = (
            f"{car.make} {car.model}"
            + (f" ({car.generation})" if car.generation else "")
            + f" {year_range}\n"
            f"  HP: {hp}, 0-60: {accel_60}s, Reliability: {rel_score}/100\n"
            f"  Market: {price_low} – {price_high}\n"
            f"  Body: {body} | {country} | {era}"
        )
        lines.append(line)
    return "\n\n".join(lines)


def _build_prompt(car_context: str, conversation: list[dict], message: str) -> str:
    history_lines = []
    for entry in conversation[:-1]:
        role = "User" if entry["role"] == "user" else "Assistant"
        history_lines.append(f"{role}: {entry['text']}")
    history_str = "\n".join(history_lines) if history_lines else "(no prior messages)"

    prompt = f"""You are a helpful car analysis assistant. The user has a collection with these cars:
{car_context}

Conversation so far:
{history_str}

User's new question: {message}

Respond helpfully. If comparing cars, cite specific numbers from the collection."""
    return prompt


def query_agent(request: Request, message: str = Form(...)) -> HTMLResponse:
    """Agent-powered query with tool calling."""
    from motorgeek.core.agent import AgentLoop
    from motorgeek.core.database import get_session as db_session

    message = message.strip()
    if not message:
        return HTMLResponse("<p>Please enter a question.</p>")

    conversation = request.session.get("conversation", [])
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        try:
            from motorgeek.core.llm import _load_config
            config = _load_config()
            api_key = config.get("llm", {}).get("api_key", "")
        except Exception:
            pass

    if not api_key:
        agent_text = "LLM not configured. Set DEEPSEEK_API_KEY or configure config.yaml."
        result = {}
    else:
        db = db_session()
        cars = db.query(Car).all()
        if not cars:
            agent_text = "Your collection is empty. Add some cars first."
            result = {}
        else:
            car_context = _build_car_context(cars)
            system_prompt = f"""You are a helpful car analysis assistant with access to a car collection. You have tools to search, compare, and analyze cars. Use them to answer the user's questions.

Current collection:
{car_context}

Use tools when they would help. For comparisons, use list_all_cars or compare_cars. Be concise and data-driven."""

            try:
                agent = AgentLoop()
                result = agent.run(
                    system_prompt=system_prompt,
                    user_message=message,
                    conversation=conversation,
                    db=db,
                )
                agent_text = result["final_response"]
            except Exception as e:
                agent_text = f"Agent error: {e}. Try again with a simpler question."
                result = {}

    if agent_text is None:
        agent_text = "Sorry, I couldn't process that. Try again."

    # Extract tool calls from agent result
    tool_calls_display = []
    if result and "messages" in result:
        for msg in result["messages"]:
            if msg.get("role") == "assistant" and msg.get("tool_calls"):
                for tc in msg["tool_calls"]:
                    tool_calls_display.append({
                        "role": "tool",
                        "tool_name": tc["function"]["name"],
                        "tool_result": tc["function"]["arguments"],
                    })

    now = datetime.now(timezone.utc).isoformat()
    conv_msg = {"role": "user", "text": message, "timestamp": now}
    conversation.append(conv_msg)
    for tc in tool_calls_display:
        conversation.append(tc)
    conversation.append({"role": "agent", "text": agent_text, "timestamp": now})
    request.session["conversation"] = conversation

    is_htmx = request.headers.get("HX-Request") == "true"
    if is_htmx:
        # Return just the updated chat messages as HTML
        return templates.TemplateResponse(request, "query/_chat.html", {
            "conversation": conversation,
        })
    return templates.TemplateResponse(request, "query/index.html", {
        "cars": [], "conversation": conversation,
    })