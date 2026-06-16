import re, sqlite3

db = sqlite3.connect('data/motorgeek.db')

patterns = [
    # Toyota/Lexus
    (r'2GR-F[EKS]', '2GR'), (r'3UR-FE', '3UR'), (r'1GR-FE', '1GR'),
    (r'1UR-FE', '1UR'), (r'3UZ', '3UZ'), (r'1UZ', '1UZ'),
    (r'A25A-FXS', 'A25A'), (r'2AR-F[EX]', '2AR'),
    # BMW
    (r'\bB58\b', 'B58'), (r'N52', 'N52'), (r'N55', 'N55'),
    (r'N63', 'N63'), (r'M62', 'M62'), (r'B48', 'B48'),
    # Mercedes
    (r'M17[678]', 'M176'), (r'M278', 'M278'), (r'M273', 'M273'),
    (r'M276', 'M276'), (r'M117', 'M117'), (r'M113', 'M113'),
    (r'M120', 'M120'), (r'M119', 'M119'), (r'M116', 'M116'),
    (r'M104', 'M104'), (r'M111', 'M111'), (r'M112', 'M112'),
    # Audi/VW
    (r'EA839', 'EA839'), (r'EA837', 'EA837'), (r'CGWA', 'CGWA'),
    (r'BFL', 'BFL'), (r'BFM', 'BFM'),
    # GM
    (r'\bLS3\b', 'LS3'), (r'\bL86\b', 'L86'), (r'\bLGX\b', 'LGX'),
    (r'\bLFX\b', 'LFX'), (r'\bLS6\b', 'LS6'),
    # Honda
    (r'K20C', 'K20C'), (r'K24[WZ]', 'K24'), (r'J35[YZX]', 'J35'),
    (r'L15[ABC]', 'L15'), (r'LFA1', 'LFA1'), (r'R18', 'R18'),
    # Subaru
    (r'EJ25[0-9]?', 'EJ25'), (r'EJ22', 'EJ22'), (r'EJ20', 'EJ20'),
    (r'FA20', 'FA20'), (r'FB25', 'FB25'),
    # Ford/Lincoln
    (r'EcoBoost', 'EcoBoost'),
    # Nissan
    (r'VR30', 'VR30'), (r'VR38', 'VR38'), (r'VQ35', 'VQ35'),
    (r'VK56', 'VK56'), (r'SR20', 'SR20'),
    # Chrysler/FCA
    (r'Pentastar', 'Pentastar'), (r'HEMI', 'HEMI 5.7'),
    # Mazda
    (r'Skyactiv', 'Skyactiv-G'), (r'L3-V[DT]', 'DISI Turbo'),
    # Porsche
    (r'9A2', '9A2'), (r'M96', 'M96'), (r'M97', 'M97'),
    # Hyundai/Kia
    (r'G6DC', 'G6DC'), (r'Lambda', 'Lambda'),
    (r'Smartstream', 'Smartstream 3.5'),
    # Volvo
    (r'B4204', 'B4204'),
    # Mitsubishi
    (r'4B11T', '4B11T'), (r'4G63', '4G63'),
]

rows = db.execute("SELECT car_id, engine_layout FROM powertrain_ice WHERE engine_code IS NULL AND engine_layout IS NOT NULL").fetchall()
updated = 0
for car_id, layout in rows:
    for pattern, code in patterns:
        if re.search(pattern, layout, re.IGNORECASE):
            db.execute("UPDATE powertrain_ice SET engine_code = ? WHERE car_id = ?", (code, car_id))
            updated += 1
            break

db.commit()

total, filled = db.execute("SELECT COUNT(*), COUNT(engine_code) FROM powertrain_ice").fetchone()
print(f"Pass 2: {updated} updated. Coverage: {filled}/{total} ({round(100.0*filled/total, 1)}%)")

# Still missing
print("\nStill ungapped:")
for row in db.execute("SELECT DISTINCT engine_layout FROM powertrain_ice WHERE engine_code IS NULL AND engine_layout IS NOT NULL ORDER BY engine_layout"):
    print(f"  {row[0]}")
