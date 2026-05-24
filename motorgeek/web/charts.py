# motorgeek/web/charts.py

def build_radar_data(cars: list, perf_data: dict, rel_data: dict, cost_data: dict) -> dict:
    labels = ["Performance", "Engineering", "Reliability", "Cost-to-Own", "Historical"]
    datasets = []
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
    for i, car in enumerate(cars):
        perf = perf_data.get(car.id)
        rel = rel_data.get(car.id)
        cost = cost_data.get(car.id)
        perf_score = max(0, min(100, (15 - (perf.accel_0_60 or 10)) / 15 * 100)) if perf and perf.accel_0_60 else 50
        rel_score = rel.reliability_score if rel and rel.reliability_score else 50
        cost_score = max(0, min(100, 100 - (cost.depreciation_5yr_pct or 50))) if cost and cost.depreciation_5yr_pct else 50
        data = [perf_score, 70, rel_score, cost_score, 60]
        datasets.append({
            "label": f"{car.make} {car.model}",
            "data": data,
            "backgroundColor": f"{colors[i % len(colors)]}66",
            "borderColor": colors[i % len(colors)],
            "borderWidth": 2,
        })
    return {"labels": labels, "datasets": datasets}