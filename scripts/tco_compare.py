cars = [
    # Tau 5.0 runs on REGULAR 87 octane (owner's manual confirmed)
    # B58 requires PREMIUM 91+ octane
    # Regular ~$3.20/gal, Premium ~$3.80/gal (typical US spread)
    {'name': 'G90 5.0 Tau', 'city': 16, 'hwy': 24, 'maint': 900, 'fuel_price': 3.20, 'msrp': 70000, 'dep_pct': 0.65, 'max_life': 175},
    {'name': 'G80 5.0 Tau', 'city': 16, 'hwy': 24, 'maint': 900, 'fuel_price': 3.20, 'msrp': 62000, 'dep_pct': 0.60, 'max_life': 175},
    {'name': '540i pre-LCI', 'city': 22, 'hwy': 30, 'maint': 850, 'fuel_price': 3.80, 'msrp': 57200, 'dep_pct': 0.55, 'max_life': 250},
    {'name': '540i LCI',     'city': 22, 'hwy': 32, 'maint': 750, 'fuel_price': 3.80, 'msrp': 60900, 'dep_pct': 0.50, 'max_life': 250},
]

print(f"{'Car':15s} | {'Fuel/yr':>8s} | {'Maint/yr':>8s} | {'5yr OpCost':>10s} | {'Deprec':>8s} | {'Total 5yr':>10s} | {'Max Life':>8s}")
print("-" * 95)

for c in cars:
    gallons_per_yr = 12000 * (0.55/c['city'] + 0.45/c['hwy'])
    annual_fuel = gallons_per_yr * c['fuel_price']
    annual_total = annual_fuel + c['maint']
    five_yr_tco = annual_total * 5
    depreciation = c['msrp'] * c['dep_pct']
    total = five_yr_tco + depreciation
    print(f"{c['name']:15s} | ${annual_fuel:>7,.0f} | ${c['maint']:>7,} | ${five_yr_tco:>9,.0f} | ${depreciation:>7,.0f} | ${total:>9,.0f} | ~{c['max_life']}K mi")

print()
print("USED BUYER PERSPECTIVE (buying at 60K miles, driving to max life):")
print(f"{'Car':15s} | {'Used Price':>10s} | {'Yrs to Max':>10s} | {'Fuel+Maint Total':>16s} | {'Total Cost':>10s} | {'Cost/Mile':>10s}")
print("-" * 85)

used = [
    {'name': 'G90 5.0 Tau', 'used_price': 18000, 'city': 16, 'hwy': 24, 'maint': 1000, 'fuel_price': 3.20, 'start_mi': 60, 'max_life': 175},
    {'name': 'G80 5.0 Tau', 'used_price': 16000, 'city': 16, 'hwy': 24, 'maint': 1000, 'fuel_price': 3.20, 'start_mi': 60, 'max_life': 175},
    {'name': '540i pre-LCI', 'used_price': 25000, 'city': 22, 'hwy': 30, 'maint': 1100, 'fuel_price': 3.80, 'start_mi': 60, 'max_life': 250},
    {'name': '540i LCI',     'used_price': 32000, 'city': 22, 'hwy': 32, 'maint': 950,  'fuel_price': 3.80, 'start_mi': 60, 'max_life': 250},
]

for c in used:
    miles_remaining = (c['max_life'] - c['start_mi']) * 1000
    years = miles_remaining / 12000
    gallons_per_yr = 12000 * (0.55/c['city'] + 0.45/c['hwy'])
    annual_fuel = gallons_per_yr * c['fuel_price']
    total_op = (annual_fuel + c['maint']) * years
    total_cost = c['used_price'] + total_op
    cost_per_mile = total_cost / miles_remaining
    print(f"{c['name']:15s} | ${c['used_price']:>9,} | {years:>9.1f}yr | ${total_op:>15,.0f} | ${total_cost:>9,.0f} | ${cost_per_mile:>8.2f}/mi")
