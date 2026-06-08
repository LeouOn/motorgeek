# The real buyer profile: buy at the bottom of depreciation, extract last 30K miles
# Tau 5.0 at ~130K mi, B58 at ~180K mi (both near end of life but still running)

print("DEPRECIATION-BOTTOM BUYER: Buy at high mileage, drive 30K more miles")
print(f"{'Car':20s} | {'Buy Price':>10s} | {'Odo':>6s} | {'Fuel/30K':>9s} | {'Maint/30K':>10s} | {'Risk Cost':>10s} | {'Total 30K':>10s} | {'$/mile':>8s}")
print("-" * 110)

# Risk cost = expected value of catastrophic failure during ownership
# Tau 5.0: higher risk of parts unavailability, oil pump etc
# B58: lower risk, predictable failures, parts available

scenarios = [
    {
        'name': 'G90 5.0 Tau',
        'buy_price': 10000,   # 2017-2018 at ~130K miles
        'odo': '130K',
        'fuel_30k': 30 * 1000 / 18 * 3.20,  # 18mpg combined, regular
        'maint_30k': 2500,     # Higher maint at this age
        'risk_cost': 2500,     # Oil pump/timing risk ~$3K with 15-20% probability
    },
    {
        'name': 'G80 5.0 Tau',
        'buy_price': 8500,    # 2017-2020 at ~130K miles
        'odo': '130K',
        'fuel_30k': 30 * 1000 / 19 * 3.20,  # slightly lighter, ~19mpg
        'maint_30k': 2200,
        'risk_cost': 2000,
    },
    {
        'name': '540i pre-LCI',
        'buy_price': 14000,   # 2017-2019 at ~180K miles (they hold value better)
        'odo': '180K',
        'fuel_30k': 30 * 1000 / 25 * 3.80,  # 25mpg combined, premium
        'maint_30k': 3000,    # B58 stuff at 180K: water pump round 2, gaskets, etc
        'risk_cost': 1000,    # Well-documented failures, parts everywhere
    },
    {
        'name': '540i LCI',
        'buy_price': 18000,   # 2021-2023 at ~160K miles (newer, holds value)
        'odo': '160K',
        'fuel_30k': 30 * 1000 / 26 * 3.80,
        'maint_30k': 2500,
        'risk_cost': 800,
    },
]

for s in scenarios:
    total = s['buy_price'] + s['fuel_30k'] + s['maint_30k'] + s['risk_cost']
    cost_per_mile = total / 30000
    print(f"{s['name']:20s} | ${s['buy_price']:>9,} | {s['odo']:>6s} | ${s['fuel_30k']:>8,.0f} | ${s['maint_30k']:>9,} | ${s['risk_cost']:>9,} | ${total:>9,.0f} | ${cost_per_mile:>6.2f}")

print()
print("=== THE REAL QUESTION: What if it DIES before 30K? ===")
print()
print(f"{'Car':20s} | {'Buy Price':>10s} | {'Dies at':>8s} | {'Miles got':>10s} | {'Total spent':>11s} | {'$/mile':>8s} | {'Scrap value':>11s} | {'Net $/mile':>10s}")
print("-" * 115)

death_scenarios = [
    # Worst case: engine dies at 10K miles into ownership
    {'name': 'G80 5.0 Tau', 'buy': 8500, 'dies_at': 10000, 'fuel': 10000/19*3.20, 'maint': 800, 'scrap': 1500},
    {'name': '540i pre-LCI', 'buy': 14000, 'dies_at': 10000, 'fuel': 10000/25*3.80, 'maint': 800, 'scrap': 2500},
    {'name': '540i LCI',     'buy': 18000, 'dies_at': 10000, 'fuel': 10000/26*3.80, 'maint': 600, 'scrap': 3500},
]

for d in death_scenarios:
    total_spent = d['buy'] + d['fuel'] + d['maint']
    net = total_spent - d['scrap']
    cost_per_mile = net / d['dies_at']
    print(f"{d['name']:20s} | ${d['buy']:>9,} | {d['dies_at']/1000:.0f}K mi | {d['dies_at']/1000:.0f}K mi | ${total_spent:>10,.0f} | ${cost_per_mile:>6.2f} | ${d['scrap']:>10,} | ${net:>9,.0f}")
