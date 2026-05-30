import sqlite3

from motorgeek.core.database import get_session
from motorgeek.core.models import (
    Electronics, ConsumablesAndSpecs,
)

DB_PATH = "data/motorgeek.db"


def seed(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DELETE FROM performance")
    cur.executemany(
        "INSERT INTO performance (car_id, source, accel_0_60, accel_0_100, quarter_mile_time, quarter_mile_speed, top_speed_mph, power_to_weight, lateral_g, braking_60_0_ft, lap_times) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        [
            (2, "sample", 4.2, 9.5, 12.3, 112.0, 189.0, 272.73, 0.87, None, None),
            (3, "sample", 4.6, 10.5, 13.1, 109.0, 155.0, 240.80, 0.89, None, None),
            (4, "sample", 4.6, 10.2, 13.0, 107.0, 160.0, 207.64, 0.82, None, None),
            (5, "sample", 4.5, 8.8, 12.7, 115.0, 183.0, 279.36, 0.91, None, None),
            (6, "sample", 5.8, 11.8, 14.2, 101.0, 150.0, 159.68, 0.84, None, None),
            (7, "sample", 5.0, 11.0, 13.5, 104.0, 155.0, 190.20, 0.77, None, None),
        ],
    )
    print("  Seeded performance: 6 rows")

    cur.execute("DELETE FROM powertrain_ice")
    cur.executemany(
        "INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, redline_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, weight_dist_pct, suspension_fr, brakes_fr, drag_coefficient, is_hybrid, ground_clearance_mm, cargo_volume_liters) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            (2, "sample", "Flat-6", 3387.0, 6, "Twin-turbo", 420.0, 5700, 563.0, 4800, 6800, 9.4, "MFI", "6-speed manual", 6, "RWD", 1540.0, "40/60", "McPherson struts", "vented disc", 0.30, 0, 120, 100.0),
            (3, "sample", "V8", 3246.0, 8, "Naturally aspirated", 360.0, 7900, 365.0, 4900, 8000, 11.5, "MFI", "6-speed manual", 6, "RWD", 1495.0, "51/49", "MacPherson struts", "vented disc", 0.31, 0, 115, 280.0),
            (4, "sample", "Inline-6", 2997.0, 6, "Single turbo", 326.0, 5600, 435.0, 4500, 6800, 8.0, "D4-DI", "6-speed manual", 6, "RWD", 1570.0, "53/47", "MacPherson struts", "vented disc", 0.29, 0, 130, 195.0),
            (5, "sample", "V8", 3506.0, 8, "Naturally aspirated", 380.0, 8200, 363.0, 5850, 8700, 11.0, "F1-type", "6-speed manual", 6, "RWD", 1350.0, "43/57", "Wishbone", "vented disc", 0.27, 0, 110, 230.0),
            (6, "sample", "Inline-4", 1997.0, 4, "Naturally aspirated", 240.0, 8300, 208.0, 7500, 9000, 11.1, "MFI", "6-speed manual", 6, "RWD", 1500.0, "50/50", "Double wishbone", "vented disc", 0.33, 0, 125, 215.0),
            (7, "sample", "V8", 4982.0, 8, "Naturally aspirated", 322.0, 5700, 480.0, 3900, 6500, 11.0, "KE-Jetronic", "4-speed auto", 4, "RWD", 1700.0, "52/48", "W126-style", "vented disc", 0.31, 0, 140, 510.0),
        ],
    )
    print("  Seeded powertrain_ice: 6 rows")

    cur.execute("DELETE FROM reliability")
    cur.executemany(
        "INSERT INTO reliability (car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues) VALUES (?,?,?,?,?,?,?,?,?)",
        [
            (2, "sample", 68, '{"IMS bearing": 3, "bore scoring": 2}', 2000.0, 2, "Good (specialist tons)", "Difficult (rear engine)", '{"IMS bearing failure": "Carry spare.", "bore scoring": "Monitor oil temp."}'),
            (3, "sample", 72, '{"VANOS failure": 4, "subframe cracks": 3}', 2500.0, 3, "Good (BMW parts)", "Moderate (engine bay tight)", '{"VANOS codes": "Inspect at 80k mi.", "subframe plate cracking": "Race cars mostly."}'),
            (4, "sample", 88, '{"boost leaks": 2, "fuel pump": 2}', 850.0, 1, "Good (Toyota + afrmarket)", "Moderate (turbo access)", '{"2JZ-GTE nearly indestructible": "Check ancillary systems."}'),
            (5, "sample", 62, '{"timing belt tensioner": 4, "water pump": 3}', 1500.0, 2, "Moderate (Ferrari specialist)", "Difficult (mid-rear engine)", '{"timing belt tensioner failure": "Replace at 15k mi.", "water pump": "Replace with metal OEM."}'),
            (6, "sample", 78, '{"clutch fan": 2, "hardtop recall": 1}', 1100.0, 1, "Good (Honda + aftermarket)", "Moderate (F20C accessible)", '{"clutch fan": "Replace at 50k mi preventatively."}'),
            (7, "sample", 75, '{"brake vacuum booster": 3, "level regulation": 3}', 1300.0, 2, "Good (Mercedes specialist)", "Difficult (wide hood)", '{"brake booster cracking": "Common on high-mile W140s."}'),
        ],
    )
    print("  Seeded reliability: 6 rows")

    cur.execute("DELETE FROM market_history")
    cur.executemany(
        "INSERT INTO market_history (car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site) VALUES (?,?,?,?,?,?,?)",
        [
            (2, "2026-05-01", 45000.0, 85000.0, 12, "rising", "Hagerty"),
            (3, "2026-05-01", 32000.0, 55000.0, 8, "rising", "Hagerty"),
            (4, "2026-05-01", 38000.0, 65000.0, 6, "rising", "Hagerty"),
            (5, "2026-05-01", 88000.0, 145000.0, 4, "rising", "BaT"),
            (6, "2026-05-01", 22000.0, 38000.0, 10, "stable", "Hagerty"),
            (7, "2026-05-01", 12000.0, 22000.0, 5, "stable", "Hagerty"),
        ],
    )
    print("  Seeded market_history: 6 rows")

    cur.execute("DELETE FROM cost_to_own")
    cur.executemany(
        "INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, msrp_inflation_adj, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, insurance_group, depreciation_5yr_pct) VALUES (?,?,?,?,?,?,?,?,?,?)",
        [
            (2, "sample", 82500.0, "USD", 148500.0, 17.0, 24.0, 1200.0, "18", 30.0),
            (3, "sample", 46000.0, "USD", 76200.0, 16.0, 24.0, 1100.0, "17", 35.0),
            (4, "sample", 55000.0, "USD", 103950.0, 17.0, 24.0, 900.0, "15", 28.0),
            (5, "sample", 95000.0, "USD", 179550.0, 13.0, 19.0, 2200.0, "21", 25.0),
            (6, "sample", 33000.0, "USD", 54780.0, 19.0, 28.0, 850.0, "14", 38.0),
            (7, "sample", 112000.0, "USD", 211520.0, 14.0, 18.0, 1100.0, "17", 45.0),
        ],
    )
    print("  Seeded cost_to_own: 6 rows")

    cur.execute("DELETE FROM dimensions")
    cur.executemany(
        "INSERT INTO dimensions (car_id, length_mm, width_mm, height_mm, wheelbase_mm, track_front_mm, track_rear_mm, front_overhang_mm, rear_overhang_mm, source) VALUES (?,?,?,?,?,?,?,?,?,?)",
        [
            (2, 4435, 1830, 1295, 2350, 1465, 1500, None, None, "sample"),
            (3, 4492, 1780, 1372, 2731, 1508, 1525, None, None, "sample"),
            (4, 4515, 1810, 1275, 2550, 1520, 1525, None, None, "sample"),
            (5, 4477, 1922, 1214, 2600, 1669, 1617, None, None, "sample"),
            (6, 4135, 1750, 1285, 2400, 1470, 1510, None, None, "sample"),
            (7, 5113, 1886, 1486, 3040, 1603, 1576, None, None, "sample"),
        ],
    )
    print("  Seeded dimensions: 6 rows")

    cur.execute("DELETE FROM performance_measurements")
    cur.executemany(
        "INSERT INTO performance_measurements (car_id, metric_name, value, unit, source_site, sample_size, conditions) VALUES (?,?,?,?,?,?,?)",
        [
            (2, "accel_0_60", 4.2, "s", "Car & Driver", 5, "dry asphalt"),
            (2, "accel_0_100", 9.5, "s", "Car & Driver", 3, "dry asphalt"),
            (2, "quarter_mile_time", 12.3, "s", "MotorTrend", 2, "sea level"),
            (2, "quarter_mile_speed", 112.0, "mph", "MotorTrend", 2, "sea level"),
            (3, "accel_0_60", 4.6, "s", "Car & Driver", 5, "dry asphalt"),
            (3, "accel_0_100", 10.5, "s", "Car & Driver", 3, "dry asphalt"),
            (3, "quarter_mile_time", 13.1, "s", "MotorTrend", 1, "sea level"),
            (4, "accel_0_60", 4.6, "s", "Car & Driver", 5, "dry asphalt"),
            (4, "quarter_mile_time", 13.0, "s", "MotorTrend", 2, "sea level"),
            (5, "accel_0_60", 4.5, "s", "Car & Driver", 3, "dry asphalt"),
            (5, "quarter_mile_time", 12.7, "s", "MotorTrend", 2, "sea level"),
            (6, "accel_0_60", 5.8, "s", "Car & Driver", 3, "dry asphalt"),
            (7, "accel_0_60", 5.0, "s", "Car & Driver", 2, "dry asphalt"),
        ],
    )
    print("  Seeded performance_measurements: 13 rows")

    conn.commit()
    conn.close()

    session = get_session()

    session.query(Electronics).delete()
    session.query(ConsumablesAndSpecs).delete()

    electronics_data = [
        Electronics(
            car_id=2, source="sample",
            ecu_type="Bosch Motronic MED 7.1.1", ecu_bitness=None,
            obd_generation="OBD-II", flashable_ecu=False,
            ecu_open_source_support="None", bus_topology="CAN 2.0",
            can_bus_present=True, can_bus_generation="CAN 2.0",
            can_bus_speed_kbps=500, can_bus_subnets=None, lin_bus_count=None,
            flexray_present=False, most_bus_present=False, ethernet_automotive=False,
            gateway_module_count=None, bus_diagrams_notes=None,
            sensor_count_total=None, o2_sensors=None, knock_sensors=None,
            camshaft_sensors=None, crankshaft_sensors=None, map_sensors=None,
            maf_sensors=None, wheel_speed_sensors=4, steering_angle_sensor=None,
            yaw_sensor=True, accelerometers=None, radar_sensors=0,
            lidar_sensors=0, ultrasonic_sensors=0, camera_sensors=0,
            rain_light_sensor=True, tpms_sensors=None, pressure_sensors=None,
            temperature_sensors=None, exhaust_sensors=None, extra_sensors={},
            electronic_throttle=True, variable_valve_timing=False,
            variable_valve_lift=False, active_exhaust_valves=False,
            active_suspension=False, active_aero=False, electronic_diff=False,
            active_engine_mounts=False, active_grille_shutters=False,
            steer_by_wire=False, brake_by_wire=False,
            alternator_output_amps=None, alternator_type=None,
            voltage_regulator=None, battery_type_oe="Lead-acid",
            battery_capacity_ah=70.0, battery_location="Trunk",
            dual_battery_setup=False, dc_dc_converter_present=False,
            total_ecu_count=None, body_control_module=None,
            transmission_tcu=None, abs_module=None, airbag_module=None,
            instrument_cluster=None, climate_control_module=None,
            seat_control_modules=None, lighting_control=None,
            module_interop_notes=None, obd_connector_location=None,
            diagnostic_protocol="OBD-II", manufacturer_diag_tool="Porsche PIWIS",
            can_bus_accessible=False, immobilizer_type=None,
            key_programming=None, security_gateway=False,
            capacitor_era="Pre-capacitor era (1990s)",
            capacitor_known_issues=None, display_degradation=None,
            wiring_harness_decay=None, connector_corrosion=None,
            pcb_conformal_coating=False, solder_whisker_risk=False,
            known_replacement_ecus=[], electronics_repairability="Moderate (specialist required)",
            extra={},
        ),
        Electronics(
            car_id=3, source="sample",
            ecu_type="Siemens MSS54", ecu_bitness=None,
            obd_generation="OBD-II", flashable_ecu=False,
            ecu_open_source_support="None", bus_topology="CAN 2.0",
            can_bus_present=True, can_bus_generation="CAN 2.0",
            can_bus_speed_kbps=500, can_bus_subnets=None, lin_bus_count=None,
            flexray_present=False, most_bus_present=False, ethernet_automotive=False,
            gateway_module_count=None, bus_diagrams_notes=None,
            sensor_count_total=None, o2_sensors=None, knock_sensors=None,
            camshaft_sensors=None, crankshaft_sensors=None, map_sensors=None,
            maf_sensors=None, wheel_speed_sensors=4, steering_angle_sensor=None,
            yaw_sensor=True, accelerometers=None, radar_sensors=0,
            lidar_sensors=0, ultrasonic_sensors=0, camera_sensors=0,
            rain_light_sensor=False, tpms_sensors=None, pressure_sensors=None,
            temperature_sensors=None, exhaust_sensors=None, extra_sensors={},
            electronic_throttle=True, variable_valve_timing=True,
            variable_valve_lift=False, active_exhaust_valves=False,
            active_suspension=False, active_aero=False, electronic_diff=False,
            active_engine_mounts=False, active_grille_shutters=False,
            steer_by_wire=False, brake_by_wire=False,
            alternator_output_amps=None, alternator_type=None,
            voltage_regulator=None, battery_type_oe="Lead-acid AGM",
            battery_capacity_ah=75.0, battery_location="Trunk",
            dual_battery_setup=False, dc_dc_converter_present=False,
            total_ecu_count=None, body_control_module=None,
            transmission_tcu=None, abs_module=None, airbag_module=None,
            instrument_cluster=None, climate_control_module=None,
            seat_control_modules=None, lighting_control=None,
            module_interop_notes=None, obd_connector_location=None,
            diagnostic_protocol="OBD-II", manufacturer_diag_tool="BMW INPA",
            can_bus_accessible=True, immobilizer_type=None,
            key_programming=None, security_gateway=False,
            capacitor_era="Early capacitor era (2000s)",
            capacitor_known_issues=None, display_degradation=None,
            wiring_harness_decay=None, connector_corrosion=None,
            pcb_conformal_coating=False, solder_whisker_risk=False,
            known_replacement_ecus=[], electronics_repairability="Good (specialist network)",
            extra={},
        ),
        Electronics(
            car_id=4, source="sample",
            ecu_type="Toyota ECS (OBD-II 1996+)", ecu_bitness=None,
            obd_generation="OBD-II", flashable_ecu=False,
            ecu_open_source_support="None", bus_topology="None",
            can_bus_present=False, can_bus_generation=None,
            can_bus_speed_kbps=None, can_bus_subnets=None, lin_bus_count=None,
            flexray_present=False, most_bus_present=False, ethernet_automotive=False,
            gateway_module_count=None, bus_diagrams_notes=None,
            sensor_count_total=None, o2_sensors=None, knock_sensors=None,
            camshaft_sensors=None, crankshaft_sensors=None, map_sensors=None,
            maf_sensors=None, wheel_speed_sensors=4, steering_angle_sensor=None,
            yaw_sensor=False, accelerometers=None, radar_sensors=0,
            lidar_sensors=0, ultrasonic_sensors=0, camera_sensors=0,
            rain_light_sensor=False, tpms_sensors=None, pressure_sensors=None,
            temperature_sensors=None, exhaust_sensors=None, extra_sensors={},
            electronic_throttle=False, variable_valve_timing=False,
            variable_valve_lift=False, active_exhaust_valves=False,
            active_suspension=False, active_aero=False, electronic_diff=False,
            active_engine_mounts=False, active_grille_shutters=False,
            steer_by_wire=False, brake_by_wire=False,
            alternator_output_amps=None, alternator_type=None,
            voltage_regulator=None, battery_type_oe="Group 35",
            battery_capacity_ah=65.0, battery_location="Trunk",
            dual_battery_setup=False, dc_dc_converter_present=False,
            total_ecu_count=None, body_control_module=None,
            transmission_tcu=None, abs_module=None, airbag_module=None,
            instrument_cluster=None, climate_control_module=None,
            seat_control_modules=None, lighting_control=None,
            module_interop_notes=None, obd_connector_location=None,
            diagnostic_protocol="OBD-II", manufacturer_diag_tool="Toyota Techstream",
            can_bus_accessible=False, immobilizer_type=None,
            key_programming=None, security_gateway=False,
            capacitor_era="Pre-CAN era",
            capacitor_known_issues=None, display_degradation=None,
            wiring_harness_decay=None, connector_corrosion=None,
            pcb_conformal_coating=False, solder_whisker_risk=False,
            known_replacement_ecus=[], electronics_repairability="Good (Toyota + aftermarket)",
            extra={},
        ),
        Electronics(
            car_id=5, source="sample",
            ecu_type="Bosch Motronic 5.2", ecu_bitness=None,
            obd_generation="OBD-II", flashable_ecu=False,
            ecu_open_source_support="None", bus_topology="K-Line (ISO 9141)",
            can_bus_present=False, can_bus_generation=None,
            can_bus_speed_kbps=None, can_bus_subnets=None, lin_bus_count=None,
            flexray_present=False, most_bus_present=False, ethernet_automotive=False,
            gateway_module_count=None, bus_diagrams_notes=None,
            sensor_count_total=None, o2_sensors=None, knock_sensors=None,
            camshaft_sensors=None, crankshaft_sensors=None, map_sensors=None,
            maf_sensors=None, wheel_speed_sensors=4, steering_angle_sensor=None,
            yaw_sensor=False, accelerometers=None, radar_sensors=0,
            lidar_sensors=0, ultrasonic_sensors=0, camera_sensors=0,
            rain_light_sensor=False, tpms_sensors=None, pressure_sensors=None,
            temperature_sensors=None, exhaust_sensors=None, extra_sensors={},
            electronic_throttle=True, variable_valve_timing=False,
            variable_valve_lift=False, active_exhaust_valves=False,
            active_suspension=False, active_aero=False, electronic_diff=False,
            active_engine_mounts=False, active_grille_shutters=False,
            steer_by_wire=False, brake_by_wire=False,
            alternator_output_amps=None, alternator_type=None,
            voltage_regulator=None, battery_type_oe="Lead-acid",
            battery_capacity_ah=70.0, battery_location="Engine bay",
            dual_battery_setup=False, dc_dc_converter_present=False,
            total_ecu_count=None, body_control_module=None,
            transmission_tcu=None, abs_module=None, airbag_module=None,
            instrument_cluster=None, climate_control_module=None,
            seat_control_modules=None, lighting_control=None,
            module_interop_notes=None, obd_connector_location=None,
            diagnostic_protocol="OBD-II", manufacturer_diag_tool="Ferrari SD1/SD2",
            can_bus_accessible=False, immobilizer_type=None,
            key_programming=None, security_gateway=False,
            capacitor_era="Pre-capacitor era (1990s)",
            capacitor_known_issues=None, display_degradation=None,
            wiring_harness_decay=None, connector_corrosion=None,
            pcb_conformal_coating=False, solder_whisker_risk=False,
            known_replacement_ecus=[], electronics_repairability="Difficult (Ferrari specialist)",
            extra={},
        ),
        Electronics(
            car_id=6, source="sample",
            ecu_type="Honda P1706/P1707", ecu_bitness=16,
            obd_generation="OBD-II", flashable_ecu=False,
            ecu_open_source_support="Limited", bus_topology="CAN 2.0",
            can_bus_present=True, can_bus_generation="CAN 2.0",
            can_bus_speed_kbps=500, can_bus_subnets=None, lin_bus_count=None,
            flexray_present=False, most_bus_present=False, ethernet_automotive=False,
            gateway_module_count=None, bus_diagrams_notes=None,
            sensor_count_total=None, o2_sensors=None, knock_sensors=None,
            camshaft_sensors=None, crankshaft_sensors=None, map_sensors=None,
            maf_sensors=None, wheel_speed_sensors=4, steering_angle_sensor=None,
            yaw_sensor=False, accelerometers=None, radar_sensors=0,
            lidar_sensors=0, ultrasonic_sensors=0, camera_sensors=0,
            rain_light_sensor=False, tpms_sensors=None, pressure_sensors=None,
            temperature_sensors=None, exhaust_sensors=None, extra_sensors={},
            electronic_throttle=True, variable_valve_timing=False,
            variable_valve_lift=False, active_exhaust_valves=False,
            active_suspension=False, active_aero=False, electronic_diff=False,
            active_engine_mounts=False, active_grille_shutters=False,
            steer_by_wire=False, brake_by_wire=False,
            alternator_output_amps=None, alternator_type=None,
            voltage_regulator=None, battery_type_oe="Flooded lead-acid",
            battery_capacity_ah=55.0, battery_location="Mid-engine bay",
            dual_battery_setup=False, dc_dc_converter_present=False,
            total_ecu_count=None, body_control_module=None,
            transmission_tcu=None, abs_module=None, airbag_module=None,
            instrument_cluster=None, climate_control_module=None,
            seat_control_modules=None, lighting_control=None,
            module_interop_notes=None, obd_connector_location=None,
            diagnostic_protocol="OBD-II", manufacturer_diag_tool="Honda HDS",
            can_bus_accessible=True, immobilizer_type=None,
            key_programming=None, security_gateway=False,
            capacitor_era="Early capacitor era (2000s)",
            capacitor_known_issues=None, display_degradation=None,
            wiring_harness_decay=None, connector_corrosion=None,
            pcb_conformal_coating=False, solder_whisker_risk=False,
            known_replacement_ecus=[], electronics_repairability="Good (Honda + forums)",
            extra={},
        ),
        Electronics(
            car_id=7, source="sample",
            ecu_type="Bosch Motronic ME 2.8.1", ecu_bitness=None,
            obd_generation="OBD-II", flashable_ecu=False,
            ecu_open_source_support="None", bus_topology="CAN 2.0",
            can_bus_present=True, can_bus_generation="CAN 2.0",
            can_bus_speed_kbps=500, can_bus_subnets=None, lin_bus_count=None,
            flexray_present=False, most_bus_present=False, ethernet_automotive=False,
            gateway_module_count=None, bus_diagrams_notes=None,
            sensor_count_total=None, o2_sensors=None, knock_sensors=None,
            camshaft_sensors=None, crankshaft_sensors=None, map_sensors=None,
            maf_sensors=None, wheel_speed_sensors=4, steering_angle_sensor=None,
            yaw_sensor=False, accelerometers=None, radar_sensors=0,
            lidar_sensors=0, ultrasonic_sensors=0, camera_sensors=0,
            rain_light_sensor=False, tpms_sensors=None, pressure_sensors=None,
            temperature_sensors=None, exhaust_sensors=None, extra_sensors={},
            electronic_throttle=True, variable_valve_timing=False,
            variable_valve_lift=False, active_exhaust_valves=False,
            active_suspension=False, active_aero=False, electronic_diff=False,
            active_engine_mounts=False, active_grille_shutters=False,
            steer_by_wire=False, brake_by_wire=False,
            alternator_output_amps=None, alternator_type=None,
            voltage_regulator=None, battery_type_oe="Lead-acid H7",
            battery_capacity_ah=77.0, battery_location="Engine bay",
            dual_battery_setup=False, dc_dc_converter_present=False,
            total_ecu_count=None, body_control_module=None,
            transmission_tcu=None, abs_module=None, airbag_module=None,
            instrument_cluster=None, climate_control_module=None,
            seat_control_modules=None, lighting_control=None,
            module_interop_notes=None, obd_connector_location=None,
            diagnostic_protocol="OBD-II", manufacturer_diag_tool="Mercedes DAS/XENTRY",
            can_bus_accessible=True, immobilizer_type=None,
            key_programming=None, security_gateway=False,
            capacitor_era="Early capacitor era (1990s)",
            capacitor_known_issues=None, display_degradation=None,
            wiring_harness_decay=None, connector_corrosion=None,
            pcb_conformal_coating=False, solder_whisker_risk=False,
            known_replacement_ecus=[], electronics_repairability="Moderate (Mercedes specialist)",
            extra={},
        ),
    ]

    consumables_data = [
        ConsumablesAndSpecs(
            car_id=2, source="sample",
            tire_sizes=["225/40 R18 front", "295/30 R18 rear"],
            bulb_types={"headlight": "D2S xenon", "front_turn": "P21W", "rear_turn": "P21W", "tail": "P21/5W"},
            fluid_capacities={"engine_oil_L": 7.5, "coolant_L": 11.0, "transmission_L": 2.75, "front_diff_L": 0.9, "rear_diff_L": 0.9, "brake_fluid_L": 0.6, "power_steering_L": 1.2},
            obd_protocol="OBD-II",
            lug_nut_torque_nm=130.0,
        ),
        ConsumablesAndSpecs(
            car_id=3, source="sample",
            tire_sizes=["225/45 R18 front", "255/40 R18 rear"],
            bulb_types={"headlight": "D2S xenon", "front_turn": "PY21W amber", "rear_turn": "PY21W amber", "fog": "H11"},
            fluid_capacities={"engine_oil_L": 6.5, "coolant_L": 11.5, "transmission_L": 1.75, "diff_L": 1.4, "brake_fluid_L": 0.7, "power_steering_L": 1.0},
            obd_protocol="OBD-II",
            lug_nut_torque_nm=105.0,
        ),
        ConsumablesAndSpecs(
            car_id=4, source="sample",
            tire_sizes=["255/40 R17 front", "255/40 R17 rear"],
            bulb_types={"headlight": "H4 halogen", "front_turn": "7440 amber", "rear_turn": "7440 amber", "tail": "1157"},
            fluid_capacities={"engine_oil_L": 7.0, "coolant_L": 10.5, "transmission_L": 2.5, "front_diff_L": 1.2, "rear_diff_L": 1.2, "brake_fluid_L": 0.7, "power_steering_L": 1.2},
            obd_protocol="OBD-II (1996+)",
            lug_nut_torque_nm=110.0,
        ),
        ConsumablesAndSpecs(
            car_id=5, source="sample",
            tire_sizes=["225/40 R18 front", "265/40 R18 rear"],
            bulb_types={"headlight": "H1 halogen", "front_turn": "P21W", "rear_turn": "P21W", "tail": "LED"},
            fluid_capacities={"engine_oil_L": 8.5, "coolant_L": 12.0, "transmission_L": 2.5, "diff_L": 2.0, "brake_fluid_L": 0.7},
            obd_protocol="OBD-II",
            lug_nut_torque_nm=108.0,
        ),
        ConsumablesAndSpecs(
            car_id=6, source="sample",
            tire_sizes=["205/55 R16 front", "225/50 R16 rear"],
            bulb_types={"headlight_low": "H7", "headlight_high": "H1", "front_turn": "7440A amber", "rear_turn": "7440", "side_marker": "W5W"},
            fluid_capacities={"engine_oil_L": 4.5, "coolant_L": 7.5, "transmission_L": 1.95, "diff_L": 1.4, "brake_fluid_L": 0.75, "power_steering_L": 1.1},
            obd_protocol="OBD-II",
            lug_nut_torque_nm=108.0,
        ),
        ConsumablesAndSpecs(
            car_id=7, source="sample",
            tire_sizes=["225/60 R15 front", "225/60 R15 rear"],
            bulb_types={"headlight_halogen": "9004", "headlight_xenon": "D2S", "front_turn": "1157A amber", "rear_turn": "7507A amber", "reverse": "921"},
            fluid_capacities={"engine_oil_L": 8.0, "coolant_L": 11.0, "transmission_L": 8.5, "diff_L": 1.5, "brake_fluid_L": 0.7, "power_steering_L": 1.0},
            obd_protocol="OBD-II",
            lug_nut_torque_nm=120.0,
        ),
    ]

    session.add_all(electronics_data)
    session.add_all(consumables_data)
    session.commit()
    print("  Seeded electronics: 6 rows")
    print("  Seeded consumables_and_specs: 6 rows")

    print("Seed complete.")


if __name__ == "__main__":
    seed()