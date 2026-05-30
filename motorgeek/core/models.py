import re
from datetime import datetime, timezone
from typing import Optional, Any
from sqlalchemy import ForeignKey, String, Integer, Boolean, Text, Float, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def to_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    make: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    generation: Mapped[str] = mapped_column(String(50))
    year_start: Mapped[int] = mapped_column(Integer)
    year_end: Mapped[Optional[int]] = mapped_column(Integer)
    era_tag: Mapped[Optional[str]] = mapped_column(String(50))
    character: Mapped[Optional[str]] = mapped_column(String(50))  # eco, warm, hot, hyper, luxury, classic, muscle, ev
    body_style: Mapped[Optional[str]] = mapped_column(String(50))
    country: Mapped[Optional[str]] = mapped_column(String(50))
    production_units: Mapped[Optional[int]] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_paths: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def slug(self) -> str:
        parts = [self.make, self.model, self.generation]
        return to_slug('-'.join(str(p) for p in parts if p))

    performance: Mapped[Optional["Performance"]] = relationship(
        "Performance", back_populates="car", uselist=False
    )
    powertrain_ice: Mapped[Optional["PowertrainICE"]] = relationship(
        "PowertrainICE", back_populates="car", uselist=False
    )
    powertrain_ev: Mapped[Optional["PowertrainEV"]] = relationship(
        "PowertrainEV", back_populates="car", uselist=False
    )
    reliability: Mapped[Optional["Reliability"]] = relationship(
        "Reliability", back_populates="car", uselist=False
    )
    consumables: Mapped[Optional["ConsumablesAndSpecs"]] = relationship(
        "ConsumablesAndSpecs", back_populates="car", uselist=False
    )
    cost_to_own: Mapped[Optional["CostToOwn"]] = relationship(
        "CostToOwn", back_populates="car", uselist=False
    )
    market_history: Mapped[list["MarketHistory"]] = relationship(
        "MarketHistory", back_populates="car"
    )
    repair_costs: Mapped[list["RepairCosts"]] = relationship(
        "RepairCosts", back_populates="car"
    )
    repair_catalog: Mapped[list["RepairCatalog"]] = relationship(
        "RepairCatalog", back_populates="car"
    )
    historical_context: Mapped[Optional["HistoricalContext"]] = relationship(
        "HistoricalContext", back_populates="car", uselist=False,
        foreign_keys="HistoricalContext.car_id"
    )
    mod_potential: Mapped[Optional["ModPotential"]] = relationship(
        "ModPotential", back_populates="car", uselist=False
    )
    electronics: Mapped[Optional["Electronics"]] = relationship(
        "Electronics", back_populates="car", uselist=False
    )
    data_sources: Mapped[list["DataSource"]] = relationship(
        "DataSource", back_populates="car"
    )
    llm_analyses: Mapped[list["LLMAnalyses"]] = relationship(
        "LLMAnalyses", back_populates="car"
    )
    hybrid_systems: Mapped[list["HybridSystem"]] = relationship(
        "HybridSystem", back_populates="car"
    )
    dimensions: Mapped[Optional["Dimensions"]] = relationship(
        "Dimensions", back_populates="car", uselist=False
    )
    performance_measurements: Mapped[list["PerformanceMeasurements"]] = relationship(
        "PerformanceMeasurements", back_populates="car"
    )
    zeperfs_indices: Mapped[Optional["ZePerfsIndices"]] = relationship(
        "ZePerfsIndices", back_populates="car", uselist=False
    )
    car_reviews: Mapped[list["CarReviews"]] = relationship(
        "CarReviews", back_populates="car"
    )
    ingest_sessions: Mapped[list["IngestSessions"]] = relationship(
        "IngestSessions", back_populates="car"
    )


class Performance(Base):
    __tablename__ = "performance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(200))
    accel_0_60: Mapped[Optional[float]] = mapped_column(Float)
    accel_0_100: Mapped[Optional[float]] = mapped_column(Float)
    quarter_mile_time: Mapped[Optional[float]] = mapped_column(Float)
    quarter_mile_speed: Mapped[Optional[float]] = mapped_column(Float)
    top_speed_mph: Mapped[Optional[float]] = mapped_column(Float)
    power_to_weight: Mapped[Optional[float]] = mapped_column(Float)
    lateral_g: Mapped[Optional[float]] = mapped_column(Float)
    braking_60_0_ft: Mapped[Optional[float]] = mapped_column(Float)
    lap_times: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="performance")


class PowertrainICE(Base):
    __tablename__ = "powertrain_ice"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(200))
    engine_layout: Mapped[Optional[str]] = mapped_column(String(50))
    displacement_cc: Mapped[Optional[float]] = mapped_column(Float)
    cylinders: Mapped[Optional[int]] = mapped_column(Integer)
    aspiration: Mapped[Optional[str]] = mapped_column(String(50))
    horsepower_bhp: Mapped[Optional[float]] = mapped_column(Float)
    horsepower_rpm: Mapped[Optional[int]] = mapped_column(Integer)
    torque_nm: Mapped[Optional[float]] = mapped_column(Float)
    torque_rpm: Mapped[Optional[int]] = mapped_column(Integer)
    redline_rpm: Mapped[Optional[int]] = mapped_column(Integer)
    compression_ratio: Mapped[Optional[float]] = mapped_column(Float)
    fuel_system: Mapped[Optional[str]] = mapped_column(String(100))
    transmission_type: Mapped[Optional[str]] = mapped_column(String(50))
    gear_count: Mapped[Optional[int]] = mapped_column(Integer)
    drivetrain: Mapped[Optional[str]] = mapped_column(String(50))
    curb_weight_kg: Mapped[Optional[float]] = mapped_column(Float)
    weight_dist_pct: Mapped[Optional[str]] = mapped_column(String(20))
    suspension_fr: Mapped[Optional[str]] = mapped_column(String(100))
    brakes_fr: Mapped[Optional[str]] = mapped_column(String(100))
    drag_coefficient: Mapped[Optional[float]] = mapped_column(Float)
    is_hybrid: Mapped[bool] = mapped_column(Boolean, default=False)
    hybrid_system_id: Mapped[Optional[int]] = mapped_column(ForeignKey("hybrid_systems.id"))
    ground_clearance_mm: Mapped[Optional[int]] = mapped_column(Integer)
    cargo_volume_liters: Mapped[Optional[float]] = mapped_column(Float)
    power_kw: Mapped[Optional[float]] = mapped_column(Float)
    specific_power_per_cylinder_w_cm2: Mapped[Optional[float]] = mapped_column(Float)
    bmep_bar: Mapped[Optional[float]] = mapped_column(Float)
    mean_piston_speed_m_s: Mapped[Optional[float]] = mapped_column(Float)
    engine_torque_nm: Mapped[Optional[float]] = mapped_column(Float)
    fuel_consumption_mixed_l_100km: Mapped[Optional[float]] = mapped_column(Float)
    fuel_consumption_sport_l_100km: Mapped[Optional[float]] = mapped_column(Float)
    co2_emissions_g_km: Mapped[Optional[float]] = mapped_column(Float)
    fuel_tank_capacity_l: Mapped[Optional[float]] = mapped_column(Float)
    reserve_fuel_l: Mapped[Optional[float]] = mapped_column(Float)
    top_speed_claimed_kmh: Mapped[Optional[float]] = mapped_column(Float)
    power_reserve_pct: Mapped[Optional[float]] = mapped_column(Float)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="powertrain_ice")


class PowertrainEV(Base):
    __tablename__ = "powertrain_ev"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(200))
    battery_capacity_kwh: Mapped[Optional[float]] = mapped_column(Float)
    chemistry_type: Mapped[Optional[str]] = mapped_column(String(50))
    charge_arch_volts: Mapped[Optional[float]] = mapped_column(Float)
    motor_layout: Mapped[Optional[str]] = mapped_column(String(50))
    motor_count: Mapped[Optional[int]] = mapped_column(Integer)
    horsepower_bhp: Mapped[Optional[float]] = mapped_column(Float)
    torque_nm: Mapped[Optional[float]] = mapped_column(Float)
    range_mi_epa: Mapped[Optional[float]] = mapped_column(Float)
    charge_rate_peak_kw: Mapped[Optional[float]] = mapped_column(Float)
    battery_degradation_curve: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    motor_longevity_notes: Mapped[Optional[str]] = mapped_column(Text)
    ground_clearance_mm: Mapped[Optional[int]] = mapped_column(Integer)
    cargo_volume_liters: Mapped[Optional[float]] = mapped_column(Float)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="powertrain_ev")


class HybridSystem(Base):
    __tablename__ = "hybrid_systems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    hybrid_type: Mapped[Optional[str]] = mapped_column(String(50))
    system_name: Mapped[Optional[str]] = mapped_column(String(100))
    system_generation: Mapped[Optional[str]] = mapped_column(String(50))
    power_split_ratio: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    battery_capacity_kwh: Mapped[Optional[float]] = mapped_column(Float)
    battery_chemistry: Mapped[Optional[str]] = mapped_column(String(50))
    battery_voltage_nominal: Mapped[Optional[float]] = mapped_column(Float)
    battery_cooling_type: Mapped[Optional[str]] = mapped_column(String(50))
    battery_module_count: Mapped[Optional[int]] = mapped_column(Integer)
    battery_supplier: Mapped[Optional[str]] = mapped_column(String(100))
    battery_warranty_years: Mapped[Optional[int]] = mapped_column(Integer)
    battery_warranty_miles: Mapped[Optional[int]] = mapped_column(Integer)
    motor_count: Mapped[Optional[int]] = mapped_column(Integer)
    motor_type: Mapped[Optional[str]] = mapped_column(String(50))
    motor_power_kw_total: Mapped[Optional[float]] = mapped_column(Float)
    motor_torque_nm_total: Mapped[Optional[float]] = mapped_column(Float)
    motor_position: Mapped[Optional[str]] = mapped_column(String(50))
    combined_system_power_bhp: Mapped[Optional[float]] = mapped_column(Float)
    combined_system_torque_nm: Mapped[Optional[float]] = mapped_column(Float)
    ev_only_power_bhp: Mapped[Optional[float]] = mapped_column(Float)
    ev_only_range_mi: Mapped[Optional[float]] = mapped_column(Float)
    ev_only_top_speed_mph: Mapped[Optional[float]] = mapped_column(Float)
    fuel_econ_combined_mpg: Mapped[Optional[float]] = mapped_column(Float)
    electric_consumption_wh_pm: Mapped[Optional[float]] = mapped_column(Float)
    regen_braking_power_kw: Mapped[Optional[float]] = mapped_column(Float)
    can_lock_ev_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    has_charge_sustain_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    charge_rate_max_kw: Mapped[Optional[float]] = mapped_column(Float)
    engine_engagement_strategy: Mapped[Optional[str]] = mapped_column(String(200))
    cold_weather_behavior: Mapped[Optional[str]] = mapped_column(Text)
    cvt_behavior_notes: Mapped[Optional[str]] = mapped_column(Text)
    typical_degradation_5yr_pct: Mapped[Optional[float]] = mapped_column(Float)
    degradation_knee_miles: Mapped[Optional[float]] = mapped_column(Float)
    common_failure_modes: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    system_idiosyncrasies: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="hybrid_systems")


class Reliability(Base):
    __tablename__ = "reliability"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(200))
    reliability_score: Mapped[Optional[float]] = mapped_column(Float)
    common_failures: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    avg_repair_cost: Mapped[Optional[float]] = mapped_column(Float)
    recall_count: Mapped[Optional[int]] = mapped_column(Integer)
    part_availability: Mapped[Optional[str]] = mapped_column(String(100))
    diy_friendliness: Mapped[Optional[str]] = mapped_column(String(50))
    known_issues: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="reliability")


class ConsumablesAndSpecs(Base):
    __tablename__ = "consumables_and_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(200))
    tire_sizes: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    bulb_types: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    fluid_capacities: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    obd_protocol: Mapped[Optional[str]] = mapped_column(String(50))
    lug_nut_torque_nm: Mapped[Optional[float]] = mapped_column(Float)
    known_spec_conflicts: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    technical_diagram_notes: Mapped[Optional[str]] = mapped_column(Text)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="consumables")


class CostToOwn(Base):
    __tablename__ = "cost_to_own"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(200))
    msrp_original: Mapped[Optional[float]] = mapped_column(Float)
    msrp_currency: Mapped[Optional[str]] = mapped_column(String(10))
    msrp_inflation_adj: Mapped[Optional[float]] = mapped_column(Float)
    fuel_econ_city_mpg: Mapped[Optional[float]] = mapped_column(Float)
    fuel_econ_hwy_mpg: Mapped[Optional[float]] = mapped_column(Float)
    annual_maintenance_est: Mapped[Optional[float]] = mapped_column(Float)
    insurance_group: Mapped[Optional[str]] = mapped_column(String(50))
    depreciation_5yr_pct: Mapped[Optional[float]] = mapped_column(Float)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="cost_to_own")


class MarketHistory(Base):
    __tablename__ = "market_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    date_recorded: Mapped[Optional[datetime]] = mapped_column(DateTime)
    price_low: Mapped[Optional[float]] = mapped_column(Float)
    price_high: Mapped[Optional[float]] = mapped_column(Float)
    volume_sold_est: Mapped[Optional[int]] = mapped_column(Integer)
    market_trend_indicator: Mapped[Optional[str]] = mapped_column(String(50))
    source_site: Mapped[Optional[str]] = mapped_column(String(200))
    currency: Mapped[Optional[str]] = mapped_column(String(10))
    price_eur: Mapped[Optional[float]] = mapped_column(Float)

    car: Mapped["Car"] = relationship("Car", back_populates="market_history")


class RepairCosts(Base):
    __tablename__ = "repair_costs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    mileage_at_repair: Mapped[Optional[int]] = mapped_column(Integer)
    repair_category: Mapped[Optional[str]] = mapped_column(String(100))
    repair_name: Mapped[Optional[str]] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text)
    parts_cost: Mapped[Optional[float]] = mapped_column(Float)
    labor_cost: Mapped[Optional[float]] = mapped_column(Float)
    total_cost: Mapped[Optional[float]] = mapped_column(Float)
    currency: Mapped[Optional[str]] = mapped_column(String(10))
    shop_type: Mapped[Optional[str]] = mapped_column(String(50))
    source: Mapped[Optional[str]] = mapped_column(String(200))
    is_warranty_covered: Mapped[bool] = mapped_column(Boolean, default=False)
    is_recall: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="repair_costs")


class RepairCatalog(Base):
    __tablename__ = "repair_catalog"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    repair_name: Mapped[Optional[str]] = mapped_column(String(200))
    repair_category: Mapped[Optional[str]] = mapped_column(String(100))
    avg_cost_low: Mapped[Optional[float]] = mapped_column(Float)
    avg_cost_high: Mapped[Optional[float]] = mapped_column(Float)
    currency: Mapped[Optional[str]] = mapped_column(String(10))
    frequency: Mapped[Optional[str]] = mapped_column(String(50))
    typical_mileage_range: Mapped[Optional[str]] = mapped_column(String(50))
    source: Mapped[Optional[str]] = mapped_column(String(200))
    source_url: Mapped[Optional[str]] = mapped_column(String(500))
    severity: Mapped[Optional[str]] = mapped_column(String(50))
    diy_difficulty: Mapped[Optional[str]] = mapped_column(String(50))
    tools_required: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="repair_catalog")


class HistoricalContext(Base):
    __tablename__ = "historical_context"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    design_philosophy: Mapped[Optional[str]] = mapped_column(Text)
    designer_name: Mapped[Optional[str]] = mapped_column(String(100))
    cultural_significance: Mapped[Optional[str]] = mapped_column(Text)
    racing_pedigree: Mapped[Optional[str]] = mapped_column(Text)
    innovations: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    direct_competitors: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    predecessor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cars.id"))
    successor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cars.id"))
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="historical_context", foreign_keys="HistoricalContext.car_id")


class ModPotential(Base):
    __tablename__ = "mod_potential"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    platform_limits: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    tuning_friendliness: Mapped[Optional[str]] = mapped_column(String(50))
    ecu_lock_status: Mapped[Optional[str]] = mapped_column(String(50))
    common_mods: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    aftermarket_depth: Mapped[Optional[str]] = mapped_column(String(50))
    known_gotchas: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="mod_potential")


class Electronics(Base):
    __tablename__ = "electronics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(200))
    ecu_type: Mapped[Optional[str]] = mapped_column(String(100))
    ecu_bitness: Mapped[Optional[int]] = mapped_column(Integer)
    obd_generation: Mapped[Optional[str]] = mapped_column(String(50))
    flashable_ecu: Mapped[bool] = mapped_column(Boolean, default=False)
    ecu_open_source_support: Mapped[Optional[str]] = mapped_column(String(50))
    bus_topology: Mapped[Optional[str]] = mapped_column(String(100))
    can_bus_present: Mapped[bool] = mapped_column(Boolean, default=False)
    can_bus_generation: Mapped[Optional[str]] = mapped_column(String(50))
    can_bus_speed_kbps: Mapped[Optional[int]] = mapped_column(Integer)
    can_bus_subnets: Mapped[Optional[int]] = mapped_column(Integer)
    lin_bus_count: Mapped[Optional[int]] = mapped_column(Integer)
    flexray_present: Mapped[bool] = mapped_column(Boolean, default=False)
    most_bus_present: Mapped[bool] = mapped_column(Boolean, default=False)
    ethernet_automotive: Mapped[bool] = mapped_column(Boolean, default=False)
    gateway_module_count: Mapped[Optional[int]] = mapped_column(Integer)
    bus_diagrams_notes: Mapped[Optional[str]] = mapped_column(Text)
    sensor_count_total: Mapped[Optional[int]] = mapped_column(Integer)
    o2_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    knock_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    camshaft_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    crankshaft_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    map_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    maf_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    wheel_speed_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    steering_angle_sensor: Mapped[Optional[str]] = mapped_column(String(50))
    yaw_sensor: Mapped[bool] = mapped_column(Boolean, default=False)
    accelerometers: Mapped[Optional[int]] = mapped_column(Integer)
    radar_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    lidar_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    ultrasonic_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    camera_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    rain_light_sensor: Mapped[bool] = mapped_column(Boolean, default=False)
    tpms_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    pressure_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    temperature_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    exhaust_sensors: Mapped[Optional[int]] = mapped_column(Integer)
    extra_sensors: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    electronic_throttle: Mapped[bool] = mapped_column(Boolean, default=False)
    variable_valve_timing: Mapped[bool] = mapped_column(Boolean, default=False)
    variable_valve_lift: Mapped[bool] = mapped_column(Boolean, default=False)
    active_exhaust_valves: Mapped[bool] = mapped_column(Boolean, default=False)
    active_suspension: Mapped[bool] = mapped_column(Boolean, default=False)
    active_aero: Mapped[bool] = mapped_column(Boolean, default=False)
    electronic_diff: Mapped[bool] = mapped_column(Boolean, default=False)
    active_engine_mounts: Mapped[bool] = mapped_column(Boolean, default=False)
    active_grille_shutters: Mapped[bool] = mapped_column(Boolean, default=False)
    steer_by_wire: Mapped[bool] = mapped_column(Boolean, default=False)
    brake_by_wire: Mapped[bool] = mapped_column(Boolean, default=False)
    alternator_output_amps: Mapped[Optional[int]] = mapped_column(Integer)
    alternator_type: Mapped[Optional[str]] = mapped_column(String(50))
    voltage_regulator: Mapped[Optional[str]] = mapped_column(String(50))
    battery_type_oe: Mapped[Optional[str]] = mapped_column(String(50))
    battery_capacity_ah: Mapped[Optional[float]] = mapped_column(Float)
    battery_location: Mapped[Optional[str]] = mapped_column(String(50))
    dual_battery_setup: Mapped[bool] = mapped_column(Boolean, default=False)
    dc_dc_converter_present: Mapped[bool] = mapped_column(Boolean, default=False)
    total_ecu_count: Mapped[Optional[int]] = mapped_column(Integer)
    body_control_module: Mapped[Optional[str]] = mapped_column(String(100))
    transmission_tcu: Mapped[Optional[str]] = mapped_column(String(100))
    abs_module: Mapped[Optional[str]] = mapped_column(String(100))
    airbag_module: Mapped[Optional[str]] = mapped_column(String(100))
    instrument_cluster: Mapped[Optional[str]] = mapped_column(String(100))
    climate_control_module: Mapped[Optional[str]] = mapped_column(String(100))
    seat_control_modules: Mapped[Optional[int]] = mapped_column(Integer)
    lighting_control: Mapped[Optional[str]] = mapped_column(String(100))
    module_interop_notes: Mapped[Optional[str]] = mapped_column(Text)
    obd_connector_location: Mapped[Optional[str]] = mapped_column(String(100))
    diagnostic_protocol: Mapped[Optional[str]] = mapped_column(String(50))
    manufacturer_diag_tool: Mapped[Optional[str]] = mapped_column(String(100))
    can_bus_accessible: Mapped[bool] = mapped_column(Boolean, default=False)
    immobilizer_type: Mapped[Optional[str]] = mapped_column(String(50))
    key_programming: Mapped[Optional[str]] = mapped_column(Text)
    security_gateway: Mapped[bool] = mapped_column(Boolean, default=False)
    capacitor_era: Mapped[Optional[str]] = mapped_column(String(50))
    capacitor_known_issues: Mapped[Optional[str]] = mapped_column(Text)
    display_degradation: Mapped[Optional[str]] = mapped_column(Text)
    wiring_harness_decay: Mapped[Optional[str]] = mapped_column(Text)
    connector_corrosion: Mapped[Optional[str]] = mapped_column(Text)
    pcb_conformal_coating: Mapped[bool] = mapped_column(Boolean, default=False)
    solder_whisker_risk: Mapped[bool] = mapped_column(Boolean, default=False)
    known_replacement_ecus: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    electronics_repairability: Mapped[Optional[str]] = mapped_column(String(100))
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="electronics")


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(500))
    site_name: Mapped[Optional[str]] = mapped_column(String(100))
    raw_text: Mapped[Optional[str]] = mapped_column(Text)
    parsed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    dimension: Mapped[Optional[str]] = mapped_column(String(50))

    car: Mapped["Car"] = relationship("Car", back_populates="data_sources")


class LLMAnalyses(Base):
    __tablename__ = "llm_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    dimension: Mapped[Optional[str]] = mapped_column(String(50))
    prompt_hash: Mapped[Optional[str]] = mapped_column(String(64))
    model_used: Mapped[Optional[str]] = mapped_column(String(100))
    generated_text: Mapped[Optional[str]] = mapped_column(Text)
    scores: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    car: Mapped["Car"] = relationship("Car", back_populates="llm_analyses")


class ComparisonSession(Base):
    __tablename__ = "comparison_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(200))
    car_ids: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_viewed: Mapped[Optional[datetime]] = mapped_column(DateTime)


class Dimensions(Base):
    """Canonical physical measurements for a car. One row per car."""
    __tablename__ = "dimensions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False, unique=True)
    length_mm: Mapped[Optional[int]] = mapped_column(Integer)
    width_mm: Mapped[Optional[int]] = mapped_column(Integer)
    height_mm: Mapped[Optional[int]] = mapped_column(Integer)
    wheelbase_mm: Mapped[Optional[int]] = mapped_column(Integer)
    track_front_mm: Mapped[Optional[int]] = mapped_column(Integer)
    track_rear_mm: Mapped[Optional[int]] = mapped_column(Integer)
    front_overhang_mm: Mapped[Optional[int]] = mapped_column(Integer)
    rear_overhang_mm: Mapped[Optional[int]] = mapped_column(Integer)
    source: Mapped[Optional[str]] = mapped_column(String(200))
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="dimensions")


class PerformanceMeasurements(Base):
    """Individual test result rows — each source's actual measurement with metadata."""
    __tablename__ = "performance_measurements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    source_site: Mapped[Optional[str]] = mapped_column(String(100))
    test_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    sample_size: Mapped[Optional[int]] = mapped_column(Integer)
    conditions: Mapped[Optional[str]] = mapped_column(String(200))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="performance_measurements")


class ZePerfsIndices(Base):
    """ZePerfs proprietary indices stored per car."""
    __tablename__ = "zeperfs_indices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False, unique=True)
    zeperfs_index: Mapped[Optional[float]] = mapped_column(Float)
    sportivity_index: Mapped[Optional[float]] = mapped_column(Float)
    perfs_prix_ratio: Mapped[Optional[float]] = mapped_column(Float)
    source: Mapped[Optional[str]] = mapped_column(String(100))
    recorded_date: Mapped[Optional[datetime]] = mapped_column(DateTime)

    car: Mapped["Car"] = relationship("Car", back_populates="zeperfs_indices")


class CarReviews(Base):
    """Consumer and expert reviews, ratings."""
    __tablename__ = "car_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    source_site: Mapped[Optional[str]] = mapped_column(String(100))
    rating_overall: Mapped[Optional[float]] = mapped_column(Float)
    rating_reliability: Mapped[Optional[float]] = mapped_column(Float)
    rating_performance: Mapped[Optional[float]] = mapped_column(Float)
    rating_comfort: Mapped[Optional[float]] = mapped_column(Float)
    rating_value: Mapped[Optional[float]] = mapped_column(Float)
    review_excerpt: Mapped[Optional[str]] = mapped_column(Text)
    review_url: Mapped[Optional[str]] = mapped_column(String(500))
    reviewer_name: Mapped[Optional[str]] = mapped_column(String(100))
    review_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="car_reviews")


class IngestSessions(Base):
    """Tracks the state of each paste-to-save ingestion flow."""
    __tablename__ = "ingest_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cars.id"))
    raw_paste: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(500))
    source_site: Mapped[Optional[str]] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")
    llm_model: Mapped[Optional[str]] = mapped_column(String(50))
    parsed_data: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    gaps_and_questions: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    agent_messages: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    final_car_data: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    car: Mapped[Optional["Car"]] = relationship("Car", back_populates="ingest_sessions")
    tool_calls: Mapped[list["AgentToolCallLog"]] = relationship(
        "AgentToolCallLog", back_populates="session"
    )


class AgentToolCallLog(Base):
    """Log of every tool call made by the agent loop."""
    __tablename__ = "agent_tool_calls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ingest_sessions.id"))
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    arguments: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    result: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="success")  # success | error
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    session: Mapped[Optional["IngestSessions"]] = relationship("IngestSessions", back_populates="tool_calls")