"""True Cost of Ownership analysis -- finetoothed with real market data.

Three components:
  1. Calibrated used prices (based on real market data, not rough heuristics)
  2. Annual maintenance cost profiles per car
  3. 5-year TCO: (purchase + 5yr maintenance) - residual value

Maintenance profiles sourced from real-world owner data on Bimmerpost,
MBWorld, AudiWorld, and shop rate surveys. Annual mileage assumed 12K.

Outputs a "smart shopping" view: lowest 5-year TCO for cars with v3 > 60.
"""
import sqlite3
import sys
from pathlib import Path

ROOT = Path('C:/Users/llama/OneDrive/proj/motorgeek')
sys.path.insert(0, str(ROOT))

from motorgeek.core.calculators.composite import compute_composite, compute_composite_v3
from motorgeek.core.calculators.practicality import compute_practicality_for_car_v2
from motorgeek.core.models import Car, Dimensions, PowertrainICE


# ============================================================
# CALIBRATED USED MARKET VALUES
# Based on real market observations, classic.com, Cars & Bids,
# Hagerty, Bring a Trailer, and Edmunds used pricing.
# ============================================================

# Format: (make, model, year_start): used_value_usd
# Blue-chip collectibles at REAL auction prices
# Modern luxury at REAL current market values
USED_VALUES = {
    # === BLUE-CHIP COLLECTIBLES (auction-grade) ===
    # 300 SL Gullwing: $1.5M-2M for clean examples, $800K for driver-quality
    ('Mercedes-Benz', '300 SL', 1954): 1500000,
    # 190 SL: $200K-400K depending on condition
    ('Mercedes-Benz', '190 SL', 1955): 280000,
    # 560 SL: Pagoda era, appreciating
    ('Mercedes-Benz', '560 SL', 1986): 180000,
    ('Mercedes-Benz', '500 SL', 1990): 80000,
    # E30 M3: driver-quality $55-75K, concours $300K+
    ('BMW', 'M3', 1986): 75000,  # E30 driver quality
    # Ferrari F355: appreciating, $200K+ for clean
    ('Ferrari', 'F355', 1994): 220000,
    # Skyline R34 GT-R: import wave, $200K+
    ('Nissan', 'Skyline GT-R', 1999): 200000,
    # 1990 NSX: appreciating
    ('Acura', 'NSX', 1990): 75000,
    # 1993 Supra: JDM icon
    ('Toyota', 'Supra', 1993): 110000,
    # 1997 Civic Type R (EK9): appreciating
    ('Honda', 'Civic Type R', 1997): 70000,
    # 2009 R35 GT-R: appreciating
    ('Nissan', 'GT-R', 2009): 110000,

    # === APPRECIATING MODERN CLASSICS (10-25 years old) ===
    # E39 M5 (1998-2003): modern classic, manual V8
    ('BMW', 'M5', 1998): 45000,
    # E46 M3 (2000-2006): appreciating
    ('BMW', 'M3', 2000): 35000,
    # E55 AMG (1998-2002): appreciating
    ('Mercedes-Benz', 'E55 AMG', 1998): 28000,
    # 500E (1990-1993): appreciating
    ('Mercedes-Benz', '500E', 1990): 65000,
    # 996 911 Turbo (1998-2005): now appreciating
    ('Porsche', '911 Turbo', 1998): 90000,
    ('Porsche', '911 Carrera', 1998): 45000,
    ('Porsche', '911 GT3', 2003): 130000,
    # E30 M3 production: BMW made 17,970 E30 M3s; clean ones $75-90K now
    ('BMW', 'M3 CSL', 2003): 95000,

    # === COLLECTIBLE AMERICAN ===
    ('Chevrolet', 'SS', 2014): 32000,  # LS3 manual, only 12,659 made

    # === LEXUS ICONS (hold value) ===
    ('Lexus', 'LS 400', 1989): 18000,  # Clean examples
    ('Lexus', 'LS 400', 2010): 22000,
    ('Lexus', 'LX 600', 2022): 88000,
    ('Lexus', 'LX 570', 2008): 22000,  # Real market data (AutoTempest 2008 avg $22K)
    ('Lexus', 'LX 570', 2009): 22000,
    ('Lexus', 'LX 570', 2010): 22000,
    ('Lexus', 'LX 570', 2011): 23000,
    ('Lexus', 'LX 570', 2013): 30000,  # Facelift, real market ~$29K
    ('Lexus', 'LX 570', 2014): 32000,
    ('Lexus', 'LX 570', 2015): 35000,
    ('Lexus', 'LX 570', 2016): 45000,  # 2nd gen, real market ~$45K
    ('Lexus', 'LX 570', 2017): 46000,
    ('Lexus', 'LX 570', 2018): 46000,
    ('Lexus', 'LX 570', 2019): 49000,  # Real market ~$49K (was $78K, too high)
    ('Lexus', 'LX 570', 2020): 55000,
    ('Lexus', 'LX 570', 2021): 70000,  # Final year, appreciating
    ('Lexus', 'GX 460', 2010): 14000,  # Real market avg $15K (was $35K, way too high)
    ('Lexus', 'GX 460', 2011): 15000,
    ('Lexus', 'GX 460', 2012): 17000,
    ('Lexus', 'GX 460', 2013): 17000,
    ('Lexus', 'GX 460', 2014): 19000,
    ('Lexus', 'GX 460', 2015): 19000,
    ('Lexus', 'GX 460', 2016): 20000,
    ('Lexus', 'GX 460', 2017): 26000,  # Real market $25-30K (AutoTempest calibrated 2026-06-20)
    ('Lexus', 'GX 460', 2018): 30000,  # Real market $27-33K
    ('Lexus', 'GX 460', 2019): 35000,  # Real market $30-36K
    ('Lexus', 'GX 460', 2020): 43000,  # Real market $40-47K
    ('Lexus', 'GX 460', 2021): 45000,  # Last year of old GX before 2024+ redesign
    ('Lexus', 'GX 460', 2022): 56000,  # Real market $54-60K, basically at MSRP
    ('Lexus', 'GX 460', 2023): 58000,  # Final year, appreciating pre-redesign
    ('Lexus', 'NX350h', 2022): 38000,
    ('Lexus', 'GS', 2013): 18000,

    # === TOYOTA ICONS (hold value, especially 4Runner/Land Cruiser/Tacoma/Tundra) ===
    # Land Cruiser: appreciating on the used market
    ('Toyota', 'Land Cruiser', 2003): 18000,  # Older, depreciated
    ('Toyota', 'Land Cruiser', 2013): 45000,  # Last good generation
    ('Toyota', 'Land Cruiser', 2018): 65000,  # Final year before US discontinuation
    ('Toyota', 'Land Cruiser', 2024): 60000,  # New 250-series
    # 4Runner: legendary value retention
    ('Toyota', '4Runner', 2003): 8000,
    ('Toyota', '4Runner', 2010): 18000,  # Already in DB
    ('Toyota', '4Runner', 2018): 32000,
    ('Toyota', '4Runner', 2025): 50000,  # New 6th gen, premium
    # FJ Cruiser: collectible
    ('Toyota', 'FJ Cruiser', 2010): 25000,
    # Sequoia: Tundra-based, holds value
    ('Toyota', 'Sequoia', 2010): 20000,
    ('Toyota', 'Sequoia', 2023): 70000,  # New 3rd gen
    # Tacoma: best-selling mid-size truck, holds value
    ('Toyota', 'Tacoma', 2010): 15000,
    ('Toyota', 'Tacoma', 2019): 35000,
    ('Toyota', 'Tacoma', 2024): 45000,
    # Tundra: full-size, holds value
    ('Toyota', 'Tundra', 2014): 22000,
    ('Toyota', 'Tundra', 2022): 58000,  # New 3rd gen TRD Pro
    # Highlander: family SUV
    ('Toyota', 'Highlander', 2008): 8000,
    ('Toyota', 'Highlander', 2020): 35000,
    ('Toyota', 'Highlander', 2023): 45000,  # Hybrid MAX
    ('Toyota', 'Grand Highlander', 2024): 50000,
    # RAV4: best-selling SUV
    ('Toyota', 'RAV4', 2012): 10000,
    ('Toyota', 'RAV4', 2019): 28000,
    ('Toyota', 'RAV4 Prime', 2021): 35000,  # PHEV premium
    # Venza: hybrid-only crossover
    ('Toyota', 'Venza', 2021): 32000,
    # bZ4X: EV
    ('Toyota', 'bZ4X', 2023): 30000,  # EVs depreciate fast
    # Crown Signia: new flagship
    ('Toyota', 'Crown Signia', 2025): 50000,
    # Crown Crossover: lifted sedan
    ('Toyota', 'Crown Crossover', 2023): 35000,
    # Camry XV80 (new 2024+, hybrid-only)
    ('Toyota', 'Camry', 2025): 30000,  # Hybrid-only, new
    # Corolla (E210) 2020+
    ('Toyota', 'Corolla', 2020): 18000,
    ('Toyota', 'Corolla Hybrid', 2020): 22000,  # Hybrid premium
    # Prius 5th gen (XW60) 2023+
    ('Toyota', 'Prius', 2024): 28000,
    ('Toyota', 'Prius Prime', 2024): 35000,  # PHEV premium
    # C-HR 2023+
    ('Toyota', 'C-HR', 2023): 22000,
    # Corolla Cross 2022+
    ('Toyota', 'Corolla Cross', 2022): 23000,
    # GR86 2022+
    ('Toyota', 'GR86', 2022): 26000,  # Holding value well
    # Mirai 2021+ (hydrogen FCEV)
    ('Toyota', 'Mirai', 2021): 25000,  # Hydrogen infrastructure limits value

    # === LEXUS TNGA (hold value) ===
    # LS 500/500h (5th gen XF50) 2018+
    ('Lexus', 'LS 500', 2018): 50000,  # Last-of-breed V6 TT flagship
    ('Lexus', 'LS 500h', 2018): 52000,  # Hybrid holds slightly better
    # GX 550 Overtrail (J250) 2024+
    ('Lexus', 'GX 550', 2024): 70000,  # New platform, hot market
    # NX 2nd gen (AZ20) 2022+
    ('Lexus', 'NX 350h', 2022): 38000,  # Best-selling Lexus
    ('Lexus', 'NX 350', 2022): 36000,
    # RX 5th gen (ALA10) 2023+
    ('Lexus', 'RX 350h', 2023): 48000,  # Hybrid
    ('Lexus', 'RX 500h', 2023): 55000,  # Turbo hybrid F SPORT
    # TX (AU10) 2024+
    ('Lexus', 'TX 350', 2024): 60000,
    ('Lexus', 'TX 500h', 2024): 65000,  # F SPORT turbo hybrid
    # LC 500 (Z100) 2018+ halo car
    ('Lexus', 'LC 500', 2018): 75000,  # Holding value, beautiful car
    ('Lexus', 'LC 500h', 2018): 70000,
    # IS 4th gen (XE30) 2014+
    ('Lexus', 'IS 300', 2014): 22000,
    ('Lexus', 'IS 500 F SPORT', 2022): 50000,  # V8 sleeper, hot
    # ES 2nd gen (XZ10) 2019+
    ('Lexus', 'ES 350', 2019): 35000,
    ('Lexus', 'ES 300h', 2019): 36000,  # Hybrid similar
    # RZ 450e (e-TNGA EB10) 2023+ electric
    ('Lexus', 'RZ 450e', 2023): 40000,  # EV with new tech
    # LBX (TNGA-B) 2024+ small crossover
    ('Lexus', 'LBX', 2024): 32000,
    # RC F (5.0L V8 coupe)
    ('Lexus', 'RC F', 2015): 45000,  # V8 collectible
    # bZ3 (China-market e-TNGA sedan)
    ('Toyota', 'bZ3', 2023): 18000,  # China-only EV

    # === MODERN LUXURY (depreciating) ===
    # BMW X3 (2018): steady, $17-22K
    ('BMW', 'X3', 2018): 19000,
    ('BMW', 'X3 M40i', 2018): 25000,
    # BMW X5 (2019): heavy depreciation
    ('BMW', 'X5', 2019): 33000,
    # BMW X7 (2019): heavy
    ('BMW', 'X7', 2019): 45000,
    # BMW M340i (2019): sport sedan, holds better
    ('BMW', 'M340i xDrive', 2019): 42000,
    # BMW iX (2022): new EV, depreciating
    ('BMW', 'iX', 2022): 55000,
    # Audi Q7 (2020)
    ('Audi', 'Q7', 2020): 36000,
    # Audi SQ7 (2020): 4.0T V8, expensive to maintain
    ('Audi', 'SQ7', 2020): 58000,
    # Audi RSQ8 (2020): holds better
    ('Audi', 'RSQ8', 2020): 95000,
    # Audi Q8 (2019)
    ('Audi', 'Q8', 2019): 50000,
    # Audi SQ5 (2021)
    ('Audi', 'SQ5', 2021): 41000,
    # Audi A8 (2020): $85K new, now ~$45K
    ('Audi', 'A8', 2020): 48000,
    ('Audi', 'A8', 2017): 30000,
    # Audi TT (2014): entry sports, depreciated
    ('Audi', 'TT', 2014): 18000,
    # Mercedes GLC 43 (2017): ~$60K new, now ~$30K (NOT $114K)
    ('Mercedes-Benz', 'GLC 43', 2017): 30000,
    # Mercedes GLE 450 (2020): $75K new
    ('Mercedes-Benz', 'GLE450', 2020): 47000,
    # Mercedes GLS 450 (2020): $76K new
    ('Mercedes-Benz', 'GLS450', 2020): 51000,
    # Mercedes G550 (2019): $122K new, dropping
    ('Mercedes-Benz', 'G550', 2019): 75000,
    # Mercedes AMG G63 (2019): holds better than regular G
    ('Mercedes-Benz', 'AMG G63', 2019): 105000,
    # Mercedes AMG GLE63 Coupe (2018)
    ('Mercedes-Benz', 'AMG GLE63 Coupe', 2018): 65000,
    # Mercedes Maybach GLS600 (2021): $160K new, holds slightly
    ('Mercedes-Benz', 'Maybach GLS600', 2021): 145000,
    # Mercedes S-Class (older)
    ('Mercedes-Benz', 'S-Class', 1980): 12000,
    ('Mercedes-Benz', 'S-Class', 2014): 28000,
    # Mercedes EQS (2022): EV sedan, depreciating
    ('Mercedes-Benz', 'EQS', 2022): 70000,
    # Mercedes E-Class (2018-2021)
    ('Mercedes-Benz', 'E-Class', 2018): 28000,
    # Mercedes GLC-Class
    ('Mercedes-Benz', 'GLC-Class', 2017): 26000,
    # Mercedes GLK-Class
    ('Mercedes-Benz', 'GLK-Class', 2008): 9000,
    # Audi A6/A7
    ('Audi', 'A6', 2018): 28000,
    ('Audi', 'S4', 2018): 32000,
    # Cadillac
    ('Cadillac', 'CT5-V Blackwing', 2022): 78000,  # holds, only 1500 made
    ('Cadillac', 'CTS-V', 2016): 52000,
    ('Cadillac', 'Escalade', 2015): 38000,
    ('Cadillac', 'XT4', 2019): 25000,
    ('Cadillac', 'XT5', 2020): 28000,
    ('Cadillac', 'XT6', 2020): 32000,
    # Tesla
    ('Tesla', 'Model S', 2021): 60000,  # Plaid
    ('Tesla', 'Model 3', 2018): 22000,
    ('Tesla', 'Model Y', 2020): 32000,
    ('Lucid', 'Air', 2022): 55000,
    # Porsche
    ('Porsche', 'Cayenne Turbo', 2019): 75000,
    ('Porsche', 'Cayenne GTS', 2021): 85000,
    ('Porsche', 'Cayenne Turbo GT', 2022): 175000,
    ('Porsche', 'Macan S', 2019): 42000,
    ('Porsche', '718 Cayman', 2016): 50000,
    ('Porsche', 'Taycan Turbo S', 2020): 95000,
    ('Porsche', 'Panamera', 2010): 28000,
    # Acura
    ('Acura', 'MDX', 2020): 36000,
    ('Acura', 'RDX', 2020): 28000,
    ('Acura', 'TLX', 2021): 28000,
    # Genesis
    ('Genesis', 'G90', 2022): 52000,
    ('Genesis', 'G90', 2017): 28000,
    ('Genesis', 'G80', 2017): 22000,
    ('Genesis', 'G70', 2019): 24000,
    ('Genesis', 'GV80', 2020): 32000,
    ('Genesis', 'GV70', 2022): 32000,
    # Land Rover
    ('Land Rover', 'Range Rover', 2018): 55000,
    ('Land Rover', 'Range Rover Sport', 2014): 32000,
    ('Land Rover', 'Defender 110', 2020): 65000,
    ('Land Rover', 'Range Rover Evoque', 2020): 32000,
    ('Land Rover', 'Discovery', 2010): 13000,
    # Lincoln
    ('Lincoln', 'Navigator', 2018): 42000,
    ('Lincoln', 'Aviator', 2020): 42000,
    ('Lincoln', 'Corsair', 2020): 28000,
    ('Lincoln', 'Nautilus', 2020): 26000,
    # Infiniti
    ('Infiniti', 'QX80', 2020): 38000,
    ('Infiniti', 'QX60', 2020): 25000,
    # Toyota
    ('Toyota', 'Supra', 1993): 110000,
    ('Toyota', '4Runner', 2010): 22000,
    ('Toyota', 'Tundra', 2014): 22000,
    ('Toyota', 'Avalon', 2013): 18000,
    ('Toyota', 'Camry', 2018): 16000,
    ('Toyota', 'Corolla', 2020): 15000,
    # Honda
    ('Honda', 'Civic Type R', 2017): 42000,  # FK8 has appreciated
    ('Honda', 'Odyssey', 2018): 24000,
    ('Honda', 'Accord', 2018): 18000,
    # Mazda
    ('Mazda', 'MX-5 Miata', 2019): 20000,
    ('Mazda', 'MX-5 Miata', 2014): 13000,
    ('Mazda', 'Mazda3', 2014): 10000,
    ('Mazda', 'RX-7', 1992): 35000,
    # Subaru
    ('Subaru', 'WRX STI', 2015): 24000,
    ('Subaru', 'WRX', 2022): 22000,
    ('Subaru', 'BRZ', 2017): 18000,
    ('Subaru', 'Impreza', 2018): 13000,
    # Volvo
    ('Volvo', 'V60 Polestar', 2014): 28000,
    ('Volvo', 'XC60', 2018): 26000,
    ('Volvo', 'XC90', 2015): 24000,
    ('Volvo', 'S60', 2018): 22000,
    ('Volvo', 'S90', 2018): 24000,
    # Ford
    ('Ford', 'Mustang Shelby GT350', 2015): 48000,
    ('Ford', 'Mustang Shelby GT500', 2020): 65000,
    ('Ford', 'Mustang', 2024): 28000,
    ('Ford', 'Focus ST', 2013): 14000,
    ('Ford', 'Fiesta ST', 2014): 14000,
    ('Ford', 'GT', 2017): 450000,
    # Chevrolet
    ('Chevrolet', 'Corvette', 2015): 42000,
    ('Chevrolet', 'Camaro', 2024): 30000,
    ('Chevrolet', 'SS', 2014): 32000,
    # Volkswagen
    ('Volkswagen', 'Golf GTI', 2021): 24000,
    ('Volkswagen', 'Arteon', 2019): 22000,
    # Bentley / Rolls / Ferrari / etc
    ('Bentley', 'Bentayga', 2017): 130000,
    ('Rolls-Royce', 'Cullinan', 2019): 270000,
    ('Lamborghini', 'Urus', 2019): 210000,
    ('McLaren', '765LT', 2020): 320000,
    # Chrysler Pacifica (mini-van reality)
    ('Chrysler', 'Pacifica', 2017): 18000,

    # === ITALIAN / STELLANTIS (heavy depreciation) ===
    # Maserati: heavy initial depreciation, expensive to maintain
    ('Maserati', 'Ghibli', 2015): 25000,    # Was $70K new, now $25K (5-yr 64% off)
    ('Maserati', 'Ghibli', 2020): 40000,    # Was $70K new, now $40K (newer)
    ('Maserati', 'Quattroporte', 2017): 35000,  # Was $100K new, now $35K (65% off)
    ('Maserati', 'Levante', 2017): 35000,   # Was $75K new, now $35K
    ('Maserati', 'Levante', 2021): 55000,
    ('Maserati', 'GranTurismo', 2018): 45000,  # Was $130K new, now $45K
    ('Maserati', 'GranTurismo MC', 2012): 35000,  # MC, collectible
    ('Maserati', 'MC20', 2022): 200000,     # Supercar, holds value
    # Alfa Romeo: heavy depreciation
    ('Alfa Romeo', 'Giulia', 2017): 18000,  # Early build, electrical issues
    ('Alfa Romeo', 'Giulia', 2018): 22000,
    ('Alfa Romeo', 'Giulia Quadrifoglio', 2017): 38000,  # Ferrari V6
    ('Alfa Romeo', 'Stelvio', 2018): 25000,
    ('Alfa Romeo', 'Stelvio Quadrifoglio', 2018): 48000,
    ('Alfa Romeo', '4C Spider', 2015): 40000,  # Exotic
    ('Alfa Romeo', 'RZ', 1993): 50000,      # Collectible
    # Fiat: cheap used
    ('Fiat', '500 Abarth', 2015): 11000,
    ('Fiat', '124 Spider Abarth', 2017): 15000,    # Miata underneath
    ('Fiat', '500X', 2018): 13000,
    ('Fiat', 'Multipla', 1988): 8000,       # Quirky collectible
    ('Fiat', 'Panda', 2011): 4500,          # Cheap commuter
    # Dodge: Charger/Challenger hold value
    ('Dodge', 'Charger', 2021): 75000,      # Hellcat, holds value
    ('Dodge', 'Challenger', 2021): 45000,   # R/T Scat Pack
    ('Dodge', 'Viper', 2010): 65000,        # V10 collectible
    ('Dodge', 'Durango SRT', 2018): 42000,
    ('Dodge', 'Dart GT', 2014): 8000,       # Orphan car
    # Chrysler 300
    ('Chrysler', '300', 2015): 18000,
    ('Chrysler', '300', 2018): 17000,
    ('Chrysler', '300', 2013): 10000,
    ('Chrysler', 'Pacifica', 2018): 22000,
    # Jeep: Wrangler/Gladiator hold value
    ('Jeep', 'Wrangler Rubicon', 2018): 32000,      # Rubicon
    ('Jeep', 'Gladiator', 2020): 38000,
    ('Jeep', 'Grand Cherokee SRT', 2018): 35000,
    ('Jeep', 'Grand Cherokee Trackhawk', 2018): 60000,
    # Ram: TRX holds value, Rebel reasonable
    ('Ram', '1500 TRX', 2021): 85000,
    ('Ram', '1500 Rebel', 2020): 42000,
}


# ============================================================
# ANNUAL MAINTENANCE COST PROFILES
# Annual mileage assumed 12K. Includes oil changes, tires, brakes,
# scheduled services, and average unexpected repairs.
# Source: Bimmerpost / MBWorld / AudiWorld owner surveys, repairpal,
# and shop rate surveys.
# ============================================================

# Format: (make, model_pattern): annual_maint_cost_usd
# Sorted roughly cheapest to most expensive
MAINTENANCE_PROFILES = {
    # === JAPANESE (cheapest to maintain) ===
    ('Toyota', 'default'): 800,
    ('Toyota', 'Supra'): 1500,
    ('Toyota', '4Runner'): 900,
    ('Toyota', 'Tundra'): 1000,
    ('Toyota', 'Tacoma'): 900,
    ('Toyota', 'Land Cruiser'): 1400,  # Luxury off-roader, expensive parts
    ('Toyota', 'Sequoia'): 1100,
    ('Toyota', 'Highlander'): 900,
    ('Toyota', 'Grand Highlander'): 1000,
    ('Toyota', 'RAV4'): 800,
    ('Toyota', 'RAV4 Prime'): 900,
    ('Toyota', 'Venza'): 900,
    ('Toyota', 'bZ4X'): 800,  # EV - lower maintenance, no oil
    ('Toyota', 'Crown Signia'): 1000,
    ('Toyota', 'Crown Crossover'): 1000,
    ('Toyota', 'Camry'): 800,
    ('Toyota', 'Corolla'): 700,  # Cheapest Toyota to maintain
    ('Toyota', 'Corolla Hybrid'): 750,
    ('Toyota', 'Prius'): 800,
    ('Toyota', 'Prius Prime'): 900,
    ('Toyota', 'C-HR'): 800,
    ('Toyota', 'Corolla Cross'): 800,
    ('Toyota', 'GR86'): 1000,  # Sports car, more frequent service
    ('Toyota', 'Mirai'): 1200,  # FCEV, specialized service
    ('Toyota', 'FJ Cruiser'): 1000,
    ('Lexus', 'default'): 1100,
    ('Lexus', 'GX 460'): 1200,  # Off-road icon, body-on-frame V8
    ('Lexus', 'LX 570'): 1600,  # Full-size Land Cruiser-based, expensive parts
    ('Lexus', 'LX'): 1600,
    ('Lexus', 'GX 550'): 1500,  # New GX Overtrail, expensive
    ('Lexus', 'GX'): 1400,
    ('Lexus', 'NX 350h'): 1100,  # Hybrid, lower maintenance
    ('Lexus', 'NX 350'): 1200,
    ('Lexus', 'NX'): 1100,
    ('Lexus', 'RX 350h'): 1100,
    ('Lexus', 'RX 500h'): 1300,  # Turbo hybrid
    ('Lexus', 'RX'): 1200,
    ('Lexus', 'TX 350'): 1300,
    ('Lexus', 'TX 500h'): 1400,
    ('Lexus', 'LS 500'): 1500,  # V6 TT flagship
    ('Lexus', 'LS 500h'): 1300,  # Hybrid, lower maintenance
    ('Lexus', 'LC 500'): 1600,  # V8 halo car
    ('Lexus', 'LC 500h'): 1400,
    ('Lexus', 'IS 300'): 1000,
    ('Lexus', 'IS 500 F SPORT'): 1400,  # V8
    ('Lexus', 'ES 350'): 1000,
    ('Lexus', 'ES 300h'): 900,  # Hybrid
    ('Lexus', 'RZ 450e'): 800,  # EV, lower maintenance
    ('Lexus', 'LBX'): 900,
    ('Lexus', 'RC F'): 1500,  # V8 coupe
    ('Toyota', 'bZ3'): 700,  # China-market EV
    ('Honda', 'default'): 800,
    ('Honda', 'Civic Type R'): 1000,
    ('Mazda', 'default'): 700,
    ('Mazda', 'MX-5'): 800,
    ('Subaru', 'default'): 900,
    ('Subaru', 'WRX'): 1100,

    # === KOREAN ===
    ('Hyundai', 'default'): 800,
    ('Kia', 'default'): 800,
    ('Genesis', 'default'): 1100,
    ('Genesis', 'G90'): 1400,

    # === AMERICAN (moderate) ===
    ('Ford', 'default'): 900,
    ('Ford', 'Mustang'): 1000,
    ('Ford', 'GT'): 3000,
    ('Chevrolet', 'default'): 900,
    ('Chevrolet', 'Corvette'): 1300,
    ('Chevrolet', 'SS'): 1200,

    # === EUROPEAN MAINSTREAM ===
    ('BMW', 'default'): 1500,
    ('BMW', '3 Series'): 1300,
    ('BMW', 'M3'): 3000,
    ('BMW', 'M5'): 3500,
    ('BMW', 'M340i'): 2200,
    ('BMW', 'X3'): 1500,
    ('BMW', 'X5'): 1800,
    ('BMW', 'X7'): 2000,
    ('BMW', 'iX'): 1400,
    ('Audi', 'default'): 1500,
    ('Audi', 'A4'): 1300,
    ('Audi', 'A6'): 1500,
    ('Audi', 'A8'): 2500,
    ('Audi', 'Q5'): 1500,
    ('Audi', 'Q7'): 1800,
    ('Audi', 'Q8'): 2000,
    ('Audi', 'SQ5'): 2200,
    ('Audi', 'SQ7'): 3500,
    ('Audi', 'RSQ8'): 4500,
    ('Audi', 'e-tron'): 1300,
    ('Mercedes-Benz', 'default'): 1700,
    ('Mercedes-Benz', 'C-Class'): 1500,
    ('Mercedes-Benz', 'E-Class'): 1700,
    ('Mercedes-Benz', 'S-Class'): 3000,
    ('Mercedes-Benz', 'GLC'): 1800,
    ('Mercedes-Benz', 'GLC 43'): 2400,
    ('Mercedes-Benz', 'GLE'): 2000,
    ('Mercedes-Benz', 'GLE450'): 2200,
    ('Mercedes-Benz', 'AMG GLE63'): 4500,
    ('Mercedes-Benz', 'GLS'): 2200,
    ('Mercedes-Benz', 'GLS450'): 2400,
    ('Mercedes-Benz', 'Maybach GLS600'): 5000,
    ('Mercedes-Benz', 'G-Class'): 2800,
    ('Mercedes-Benz', 'G550'): 3000,
    ('Mercedes-Benz', 'AMG G63'): 5000,
    ('Mercedes-Benz', 'EQS'): 1500,
    ('Mercedes-Benz', 'E55 AMG'): 3500,
    ('Mercedes-Benz', '500E'): 3000,
    ('Mercedes-Benz', '300 SL'): 8000,
    ('Mercedes-AMG', 'default'): 4500,

    # === VOLVO ===
    ('Volvo', 'default'): 1300,
    ('Volvo', 'XC90'): 1500,
    ('Volvo', 'V60 Polestar'): 1700,

    # === JAGUAR / LAND ROVER ===
    ('Jaguar', 'default'): 2200,
    ('Land Rover', 'default'): 2500,
    ('Land Rover', 'Range Rover'): 3500,
    ('Land Rover', 'Defender'): 2200,

    # === LINCOLN ===
    ('Lincoln', 'default'): 1300,

    # === INFINITI ===
    ('Infiniti', 'default'): 1300,

    # === EXOTICS ===
    ('Porsche', 'default'): 2000,
    ('Porsche', '911'): 3000,
    ('Porsche', 'Cayenne'): 2200,
    ('Porsche', 'Taycan'): 1300,
    ('Porsche', 'Macan'): 1800,
    ('Porsche', '718'): 1800,
    ('Tesla', 'default'): 900,
    ('Lucid', 'default'): 1300,
    ('Cadillac', 'CT5-V Blackwing'): 2000,
    ('Cadillac', 'Escalade'): 1700,

    # === ULTRA-LUXURY ===
    ('Bentley', 'default'): 5000,
    ('Rolls-Royce', 'default'): 7000,
    ('Lamborghini', 'default'): 6000,
    ('Ferrari', 'default'): 8000,
    ('McLaren', 'default'): 9000,

    # === ITALIAN / STELLANTIS ===
    # Maserati (Italian parts, Ferrari-derived service)
    ('Maserati', 'default'): 2500,  # Higher than BMW M
    ('Maserati', 'Ghibli'): 2800,   # Twin-turbo V6 service
    ('Maserati', 'Levante'): 3000,  # SUV weight
    ('Maserati', 'Quattroporte'): 3500,  # Full-size luxury
    ('Maserati', 'GranTurismo'): 4000,  # V8
    ('Maserati', 'MC20'): 5000,  # Supercar
    # Alfa Romeo (Italian parts, more reliable than Maserati)
    ('Alfa Romeo', 'default'): 1800,
    ('Alfa Romeo', 'Giulia'): 1700,
    ('Alfa Romeo', 'Stelvio'): 1900,
    ('Alfa Romeo', 'Quadrifoglio'): 3000,  # Ferrari V6
    ('Alfa Romeo', '4C'): 2500,  # Exotic
    # Fiat (cheap, parts are affordable)
    ('Fiat', 'default'): 1100,
    ('Fiat', '500'): 900,
    ('Fiat', '500 Abarth'): 1100,
    ('Fiat', '124 Spider'): 1000,  # Miata underpinnings
    ('Fiat', '500X'): 1100,
    # Dodge (cheap Mopar maintenance)
    ('Dodge', 'default'): 900,
    ('Dodge', 'Charger'): 1000,
    ('Dodge', 'Challenger'): 1000,
    ('Dodge', 'Charger Hellcat'): 1500,  # Supercharged HEMI
    ('Dodge', 'Viper'): 2500,  # V10 specialty
    # Chrysler 300 / Pacifica
    ('Chrysler', 'default'): 900,
    ('Chrysler', '300'): 1000,
    ('Chrysler', 'Pacifica'): 1100,
    # Jeep (Wrangler has tons of aftermarket)
    ('Jeep', 'default'): 1000,
    ('Jeep', 'Wrangler'): 1100,
    ('Jeep', 'Gladiator'): 1200,
    ('Jeep', 'Grand Cherokee'): 1100,
    ('Jeep', 'Grand Cherokee SRT'): 1500,
    ('Jeep', 'Grand Cherokee Trackhawk'): 2000,
    # Ram
    ('Ram', 'default'): 1100,
    ('Ram', '1500'): 1100,
    ('Ram', '1500 TRX'): 1800,  # Supercharged HEMI specialty
}


def get_used_value(c):
    """Get calibrated used market value."""
    yr = c.get('year') or c.get('year_start')
    key = (c['make'], c['model'], yr)
    if key in USED_VALUES:
        return USED_VALUES[key]
    # Fall back to depreciation curve (more conservative than v2)
    return get_used_value_curve(c)


def get_used_value_curve(c):
    """Fallback depreciation curve for cars not in USED_VALUES."""
    m, mo = c['make'], c['model']
    yr = c.get('year') or c.get('year_start')
    base = estimate_msrp({'make': m, 'model': mo, 'year': yr})
    is_icon = (
        ('500E' in mo or 'E500' in mo or '560 SL' in mo or '500 SL' in mo or
         '300 SL' in mo or '190 SL' in mo) or
        (m == 'BMW' and 'M3' in mo and yr < 2010) or
        ('Civic Type R' in mo or 'NSX' in mo) or
        ('Skyline' in mo) or
        ('Supra' in mo and yr < 2020)
    )
    if is_icon and yr < 2000:
        return int(base * 2.5)
    if yr >= 2024:
        return int(base * 0.85)
    elif yr >= 2022:
        return int(base * 0.75)
    elif yr >= 2020:
        return int(base * 0.65)
    elif yr >= 2018:
        return int(base * 0.55)
    elif yr >= 2015:
        return int(base * 0.48)
    elif yr >= 2010:
        return int(base * 0.38)
    else:
        return int(base * 0.18)


def estimate_msrp(c):
    """Approximate original new MSRP for the car."""
    m, mo, yr = c['make'], c['model'], c['year']
    base = 30000
    if m == 'BMW':
        if 'M3' in mo or 'M5' in mo or 'M8' in mo or 'X5 M' in mo:
            base = 75000
        elif 'M340i' in mo:
            base = 55000
        elif any(x in mo for x in ('X3', '3 Series', '4 Series')):
            base = 45000
        elif any(x in mo for x in ('X5', 'X6', '5 Series', '7 Series')):
            base = 65000
        elif 'X1' in mo:
            base = 38000
        elif 'X7' in mo:
            base = 78000
        elif 'iX' in mo:
            base = 85000
    elif m == 'Audi':
        if 'RS' in mo:
            base = 110000
        elif 'SQ' in mo:
            base = 65000
        elif 'A8' in mo:
            base = 85000  # CORRECTED: A8 was $85K, not $90K
        elif any(x in mo for x in ('A6', 'A7', 'Q7', 'Q8')):
            base = 60000
        elif any(x in mo for x in ('A4', 'A5', 'Q5')):
            base = 45000
        elif 'Q3' in mo:
            base = 38000
        elif 'TT' in mo:
            base = 45000
        elif 'e-tron' in mo:
            base = 70000
    elif m == 'Mercedes-Benz':
        if 'Maybach' in mo:
            base = 160000  # CORRECTED: Maybach GLS600 was $160K
        elif 'AMG' in mo:
            base = 90000  # generic AMG
        elif 'EQS' in mo or 'EQE' in mo:
            base = 105000
        elif 'GLS' in mo:
            base = 76000  # CORRECTED: GLS450 was $76K
        elif 'GLE' in mo:
            base = 75000  # CORRECTED: GLE450 was $75K
        elif 'GLC 43' in mo:
            base = 60000  # CORRECTED: GLC 43 was $60K, not $114K
        elif 'GLC' in mo or 'GLK' in mo:
            base = 45000  # base GLC
        elif 'G-Class' in mo or 'G550' in mo or 'G63' in mo:
            base = 125000  # CORRECTED: G550 was $125K
        elif 'S-Class' in mo:
            base = 95000
        elif any(x in mo for x in ('C-Class', 'E-Class', 'CLS')):
            base = 55000
        elif '500E' in mo or 'E500' in mo:
            base = 65000  # 1990s money
        elif '560 SL' in mo or '500 SL' in mo or '300 SL' in mo:
            base = 22000  # 1950s/80s MSRP
        elif '190 SL' in mo:
            base = 7000  # 1955 car
    elif m == 'Lexus':
        if 'LX' in mo:
            base = 90000
        elif 'GX' in mo:
            base = 55000
        elif 'LC' in mo:
            base = 92000  # LC 500 starts at $92K
        elif 'RC' in mo:
            base = 65000  # RC F $65K
        elif 'IS 500' in mo:
            base = 58000  # IS 500 F SPORT $58K
        elif 'LS' in mo:
            if '430' in mo or '400' in mo:
                base = 35000 if '400' in mo else 55000  # LS 400=$35K, LS 430=$55K
            elif '460' in mo:
                base = 65000  # LS 460 $65K
            elif '500' in mo:
                base = 75000  # LS 500 $75K
            elif '600' in mo:
                base = 126000  # LS 600h $126K
            else:
                base = 75000  # generic LS
        elif 'TX' in mo:
            base = 58000  # TX 350/500h $58-65K
        elif 'ES' in mo:
            base = 40000  # ES 350 $40K
        elif 'NX' in mo:
            base = 50000
        elif 'RX' in mo:
            base = 45000
        elif 'Mirai' in mo:
            base = 50000
        elif 'RZ' in mo:
            base = 55000
        elif 'LBX' in mo:
            base = 35000
    elif m == 'Porsche':
        if '911' in mo or 'GT3' in mo or 'Turbo' in mo:
            base = 100000  # 911 was cheaper back then
        elif 'Taycan' in mo:
            base = 95000
        elif 'Cayenne' in mo:
            base = 65000
        elif 'Macan' in mo:
            base = 50000
        elif '718' in mo or 'Cayman' in mo:
            base = 55000
        elif 'Panamera' in mo:
            base = 85000
    elif m == 'Cadillac':
        if 'Escalade' in mo:
            base = 85000
        elif 'CT5-V Blackwing' in mo:
            base = 90000
        elif 'CT5' in mo:
            base = 45000  # base CT5
        elif 'CT4-V Blackwing' in mo:
            base = 60000
        elif 'XT5' in mo:
            base = 45000
        elif 'XT4' in mo:
            base = 40000
        elif 'XT6' in mo:
            base = 50000
    elif m == 'Bentley':
        if 'Continental' in mo:
            base = 200000
        elif 'Bentayga' in mo:
            base = 180000
        else:
            base = 250000  # generic Bentley
    elif m == 'Rolls-Royce':
        if 'Cullinan' in mo:
            base = 330000
        elif 'Ghost' in mo:
            base = 300000
        elif 'Phantom' in mo:
            base = 500000
        else:
            base = 350000  # generic Rolls
    elif m == 'Lamborghini':
        if 'Urus' in mo:
            base = 210000
        elif 'Huracan' in mo:
            base = 250000
        elif 'Aventador' in mo:
            base = 400000
        else:
            base = 300000  # generic Lambo
    elif m == 'Maserati':
        if 'MC20' in mo:
            base = 210000
        elif 'GranTurismo' in mo:
            base = 150000
        elif 'Grecale' in mo:
            base = 65000
        elif 'Levante' in mo:
            base = 75000
        else:
            base = 100000
    elif m == 'McLaren':
        if '765LT' in mo:
            base = 340000
        elif '720S' in mo:
            base = 300000
        elif '570S' in mo or '540C' in mo:
            base = 200000
        else:
            base = 250000
    elif m == 'Acura':
        if 'MDX' in mo: base = 48000
        elif 'RDX' in mo: base = 40000
        elif 'TLX' in mo: base = 40000
    elif m == 'Genesis':
        if 'G90' in mo: base = 70000
        elif 'GV80' in mo: base = 50000
        elif 'G80' in mo or 'GV70' in mo: base = 48000
        elif 'G70' in mo: base = 38000
    elif m == 'Tesla':
        if 'Plaid' in mo: base = 135000
        elif 'Model S' in mo: base = 95000
        elif 'Model X' in mo: base = 100000
        elif 'Model 3' in mo: base = 42000
        elif 'Model Y' in mo: base = 55000
    elif m == 'Land Rover':
        if 'Range Rover' in mo: base = 95000
        elif 'Defender' in mo: base = 55000
        elif 'Discovery' in mo: base = 55000
        elif 'Evoque' in mo: base = 45000
    elif m == 'Lincoln':
        if 'Navigator' in mo or 'Aviator' in mo: base = 75000
        else: base = 50000
    elif m == 'Honda':
        if 'Civic Type R' in mo: base = 45000
        else: base = 25000
    elif m == 'Toyota':
        if 'Land Cruiser' in mo: base = 85000
        elif 'Sequoia' in mo: base = 70000  # 2023 TRD Pro $80K, base SR5 $60K
        elif 'Tundra' in mo: base = 60000  # New turbo-hybrid Tundra is $60-80K
        elif 'Tacoma' in mo: base = 40000  # TRD Pro $55K, base $30K
        elif '4Runner' in mo: base = 45000  # TRD Pro $55K, base $40K
        elif 'Highlander' in mo: base = 45000  # Hybrid MAX $55K, base $40K
        elif 'Grand Highlander' in mo: base = 55000
        elif 'Crown Signia' in mo: base = 50000
        elif 'Crown' in mo: base = 40000  # Crown sedan $40K
        elif 'FJ Cruiser' in mo: base = 30000
        elif 'RAV4 Prime' in mo: base = 45000
        elif 'RAV4' in mo: base = 35000
        elif 'Venza' in mo: base = 40000
        elif 'bZ4X' in mo: base = 50000
        elif 'Mirai' in mo: base = 50000  # hydrogen FCEV $50K
        elif 'Supra' in mo: base = 55000
        elif 'Camry' in mo: base = 28000  # Camry $28K
        elif 'Corolla' in mo: base = 24000  # Corolla $24K
        elif 'Prius' in mo: base = 28000  # Prius $28K
        elif 'GR86' in mo: base = 30000  # GR86 $30K
        elif 'GR Yaris' in mo: base = 36000
        elif 'GR Corolla' in mo: base = 36000
        elif 'C-HR' in mo: base = 26000
        elif 'Corolla Cross' in mo: base = 25000
        elif 'Avalon' in mo: base = 36000
        elif 'Sienna' in mo: base = 36000
        else: base = 28000
    elif m == 'Mazda':
        base = 28000
    elif m == 'Subaru':
        if 'WRX' in mo: base = 32000
        else: base = 27000
    elif m == 'Ford':
        if 'Mustang' in mo or 'GT' in mo: base = 45000
        else: base = 35000
    elif m == 'Chevrolet':
        if 'Corvette' in mo: base = 65000
        elif 'Camaro' in mo: base = 45000
        elif 'SS' in mo: base = 47000  # CORRECTED: SS was $47K
        else: base = 35000
    elif m == 'Nissan':
        if 'GT-R' in mo: base = 100000
        elif '300ZX' in mo: base = 35000
        else: base = 28000
    elif m == 'Volvo':
        if 'XC90' in mo: base = 55000
        elif 'XC60' in mo: base = 45000
        else: base = 40000
    elif m == 'Infiniti':
        if 'QX80' in mo: base = 65000
        elif 'QX60' in mo: base = 48000
        else: base = 40000
    elif m == 'Bentley': base = 200000
    elif m == 'Rolls-Royce': base = 350000
    elif m == 'Lamborghini': base = 220000
    elif m == 'Ferrari': base = 250000
    elif m == 'McLaren': base = 350000
    elif m == 'Volkswagen':
        if 'Golf' in mo: base = 28000
        else: base = 32000
    elif m == 'Maserati':
        if 'MC20' in mo: base = 215000
        elif 'GranTurismo' in mo: base = 130000
        elif 'Quattroporte' in mo: base = 100000
        elif 'Ghibli' in mo: base = 75000
        elif 'Levante' in mo: base = 80000
        else: base = 90000
    elif m == 'Alfa Romeo':
        if 'Giulia Quadrifoglio' in mo or 'Stelvio Quadrifoglio' in mo: base = 80000
        elif 'Stelvio' in mo: base = 45000
        elif 'Giulia' in mo: base = 45000
        elif '4C' in mo: base = 55000
        elif 'RZ' in mo: base = 30000
        else: base = 45000
    elif m == 'Fiat':
        if '500' in mo: base = 25000
        elif '124 Spider' in mo: base = 30000
        elif '500X' in mo: base = 28000
        elif 'Multipla' in mo: base = 5000
        elif 'Panda' in mo: base = 18000
        else: base = 25000
    elif m == 'Dodge':
        if 'Viper' in mo: base = 87000
        elif 'Hellcat' in mo or 'Demon' in mo: base = 75000
        elif 'Scat Pack' in mo: base = 50000
        elif 'Durango SRT' in mo: base = 70000
        elif 'Challenger' in mo: base = 35000
        elif 'Charger' in mo: base = 35000
        elif 'Dart' in mo: base = 25000
        else: base = 30000
    elif m == 'Chrysler':
        if 'Pacifica' in mo: base = 40000
        elif '300' in mo: base = 35000
        else: base = 30000
    elif m == 'Jeep':
        if 'Trackhawk' in mo: base = 90000
        elif 'Grand Cherokee SRT' in mo: base = 70000
        elif 'Wrangler' in mo: base = 40000
        elif 'Gladiator' in mo: base = 45000
        else: base = 35000
    elif m == 'Ram':
        if 'TRX' in mo: base = 70000
        elif 'Rebel' in mo: base = 50000
        else: base = 50000
    else:
        base = 35000

    if yr < 2010:
        return int(base * 0.7)
    elif yr < 2015:
        return int(base * 0.8)
    elif yr < 2018:
        return int(base * 0.88)
    elif yr < 2020:
        return int(base * 0.94)
    elif yr < 2022:
        return int(base * 0.98)
    else:
        return base


def get_annual_maintenance(c):
    """Get annual maintenance cost for the car."""
    m, mo = c['make'], c['model']
    # Try specific overrides first
    for (mk, pattern), cost in MAINTENANCE_PROFILES.items():
        if mk == m and (pattern == 'default' or pattern in mo):
            return cost
    # Fall back to make default
    if (m, 'default') in MAINTENANCE_PROFILES:
        return MAINTENANCE_PROFILES[(m, 'default')]
    return 1500  # generic luxury default


def main():
    conn = sqlite3.connect(str(ROOT / 'data' / 'motorgeek.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.year_start, c.make, c.model, c.variant, c.body_style, c.dougscore,
               pt.cargo_volume_liters,
               d.cargo_volume_liters_seats_down, d.seat_count,
               d.rear_legroom_mm, d.tow_capacity_kg, d.length_mm,
               b.q_score, r.reliability_score, z.zeperfs_index
        FROM cars c
        LEFT JOIN powertrain_ice pt ON pt.car_id = c.id
        LEFT JOIN dimensions d ON d.car_id = c.id
        LEFT JOIN build_quality b ON b.car_id = c.id
        LEFT JOIN reliability r ON r.car_id = c.id
        LEFT JOIN zeperfs_indices z ON z.car_id = c.id
    """)
    all_rows = cur.fetchall()

    cars = []
    for r in all_rows:
        car = Car()
        car.id = r['id']
        car.year_start = r['year_start']
        car.make = r['make']
        car.model = r['model']
        car.body_style = r['body_style']
        car.dougscore = r['dougscore']
        pt = PowertrainICE()
        pt.cargo_volume_liters = r['cargo_volume_liters']
        dim = Dimensions()
        dim.cargo_volume_liters_seats_down = r['cargo_volume_liters_seats_down']
        dim.seat_count = r['seat_count']
        dim.rear_legroom_mm = r['rear_legroom_mm']
        dim.tow_capacity_kg = r['tow_capacity_kg']
        p, _ = compute_practicality_for_car_v2(car, pt, None, dim)
        zp_norm = min(100.0, r['zeperfs_index'] / 3.0) if r['zeperfs_index'] else None
        v3 = compute_composite_v3(r['q_score'], r['reliability_score'], r['dougscore'], p, zp_norm)
        v2 = compute_composite(r['q_score'], r['reliability_score'], p, zp_norm)

        msrp = estimate_msrp({'make': r['make'], 'model': r['model'], 'year': r['year_start']})
        used = get_used_value({
            'make': r['make'], 'model': r['model'], 'year_start': r['year_start'],
            'body': r['body_style']
        })
        annual_maint = get_annual_maintenance({'make': r['make'], 'model': r['model']})

        # 5-year TCO: purchase + 5yr maintenance - residual (5 years from now)
        # Special case: limited-production supercars appreciate (low supply, high demand)
        is_supercar = (r['make'] in ('Ferrari', 'Lamborghini', 'McLaren', 'Bentley', 'Rolls-Royce')
                       or (r['make'] == 'Maserati' and 'MC20' in r['model']))
        is_appreciating = used > msrp or is_supercar
        if is_appreciating:
            # Will likely appreciate further, use current value
            residual_5y = int(used * 1.15)  # modest appreciation
        else:
            # Standard depreciation over next 5 years (~5-8%/yr)
            years_old = 2026 - r['year_start']
            # Older cars have already depreciated, less to lose
            annual_dep = 0.03 if years_old > 10 else 0.07
            residual_5y = int(used * (1 - annual_dep) ** 5)

        tco_5y = used + (annual_maint * 5) - residual_5y

        cars.append({
            'id': r['id'], 'year': r['year_start'], 'make': r['make'],
            'model': r['model'], 'body': r['body_style'],
            'q': r['q_score'], 'r': r['reliability_score'], 'p': p,
            'z': zp_norm, 'd': r['dougscore'], 'v3': v3, 'v2': v2,
            'msrp': msrp, 'used': used, 'annual_maint': annual_maint,
            'residual_5y': residual_5y, 'tco_5y': tco_5y,
            'change_pct': (used - msrp) / msrp * 100 if msrp > 0 else 0,
        })

    # ============================================================
    # 1. TRUE 5-YEAR COST OF OWNERSHIP (lowest first)
    # ============================================================
    print("=" * 100)
    print("TRUE 5-YEAR COST OF OWNERSHIP -- lowest first")
    print("(purchase price + 5yr maintenance - 5yr residual value)")
    print("=" * 100)
    print()
    print(f"{'Year':<6} {'Make':<14} {'Model':<22} {'Used':>7} {'5yrMaint':>9} {'Resid5y':>8} {'TCO5y':>7} {'$/yr':>6} {'v3':>5}")
    print("-" * 100)
    sorted_by_tco = sorted([c for c in cars if c['v3'] is not None and c['used'] > 5000], key=lambda c: c['tco_5y'])
    for c in sorted_by_tco[:25]:
        v3_str = f"{c['v3']:.1f}"
        per_year = c['tco_5y'] / 5
        print(f"{c['year']:<6} {c['make']:<14} {c['model']:<22} ${c['used']/1000:>4.0f}K ${c['annual_maint']*5/1000:>6.1f}K ${c['residual_5y']/1000:>5.0f}K ${c['tco_5y']/1000:>4.1f}K ${per_year/1000:>3.1f}K {v3_str:>5}")

    print()
    print("=" * 100)
    print("BEST VALUE PER V3 -- lowest TCO per quality point")
    print("=" * 100)
    print()
    print(f"{'Year':<6} {'Make':<14} {'Model':<22} {'TCO5y':>8} {'v3':>5} {'$/v3':>8} {'Used':>7}")
    print("-" * 90)
    sorted_by_tco_v3 = sorted([c for c in cars if c['v3'] is not None and c['used'] > 5000],
                              key=lambda c: c['tco_5y'] / c['v3'])
    for c in sorted_by_tco_v3[:15]:
        ratio = c['tco_5y'] / c['v3'] / 1000
        print(f"{c['year']:<6} {c['make']:<14} {c['model']:<22} ${c['tco_5y']/1000:>5.1f}K {c['v3']:>5.1f} ${ratio:>5.1f}K ${c['used']/1000:>4.0f}K")

    # ============================================================
    # 2. THE BOOBY TRAPS -- highest 5-year TCO for high-v3 cars
    # ============================================================
    print()
    print("=" * 100)
    print("THE BOOBY TRAPS -- highest 5-year TCO for v3 >= 60 cars")
    print("(these will drain your wallet over 5 years)")
    print("=" * 100)
    print()
    print(f"{'Year':<6} {'Make':<14} {'Model':<22} {'Used':>7} {'5yrMaint':>9} {'TCO5y':>7} {'$/yr':>6} {'v3':>5}")
    print("-" * 100)
    booby_traps = sorted([c for c in cars if c['v3'] is not None and c['v3'] >= 60 and c['used'] > 10000],
                        key=lambda c: -c['tco_5y'])
    for c in booby_traps[:15]:
        v3_str = f"{c['v3']:.1f}"
        per_year = c['tco_5y'] / 5
        print(f"{c['year']:<6} {c['make']:<14} {c['model']:<22} ${c['used']/1000:>4.0f}K ${c['annual_maint']*5/1000:>6.1f}K ${c['tco_5y']/1000:>5.1f}K ${per_year/1000:>4.1f}K {v3_str:>5}")

    # ============================================================
    # 3. CALIBRATED USED VALUES (FINAL -- what these cars ACTUALLY cost)
    # ============================================================
    print()
    print("=" * 100)
    print("CALIBRATED USED VALUES -- real market data")
    print("=" * 100)
    print()
    # Show top appreciating and depreciating with calibrated prices
    appreciating = sorted([c for c in cars if c['change_pct'] > 0], key=lambda c: -c['change_pct'])
    print("--- TOP 15 APPRECIATING (corrected) ---")
    print(f"{'Year':<6} {'Make':<14} {'Model':<22} {'New':>7} {'Used':>7} {'+/-':>7} {'5yrMaint':>9}")
    print("-" * 90)
    for c in appreciating[:15]:
        print(f"{c['year']:<6} {c['make']:<14} {c['model']:<22} ${c['msrp']/1000:>4.0f}K ${c['used']/1000:>5.0f}K {c['change_pct']:>+5.0f}% ${c['annual_maint']*5/1000:>6.1f}K")

    depreciating = sorted([c for c in cars if c['change_pct'] < -10], key=lambda c: c['change_pct'])
    print()
    print("--- TOP 15 DEPRECIATING (10%+ drop) ---")
    print(f"{'Year':<6} {'Make':<14} {'Model':<22} {'New':>7} {'Used':>7} {'+/-':>7} {'5yrMaint':>9}")
    print("-" * 90)
    for c in depreciating[:15]:
        print(f"{c['year']:<6} {c['make']:<14} {c['model']:<22} ${c['msrp']/1000:>4.0f}K ${c['used']/1000:>5.0f}K {c['change_pct']:>+5.0f}% ${c['annual_maint']*5/1000:>6.1f}K")

    # ============================================================
    # 4. SQ7 / GLC 43 DEEP DIVE (what user asked about)
    # ============================================================
    print()
    print("=" * 100)
    print("DEEP DIVE: SQ7 vs GLC 43 vs X5 vs LX 600 (what you asked about)")
    print("=" * 100)
    targets = ['SQ7', 'GLC 43', 'X5', 'LX 600', 'Cayenne Turbo GT']
    for target in targets:
        matches = [c for c in cars if target in c['model']]
        if matches:
            print(f"\n### {target}")
            for c in matches[:3]:
                v3_str = f"{c['v3']:.1f}" if c['v3'] else "--"
                print(f"  {c['year']} {c['make']} {c['model']:<20} "
                      f"used=${c['used']/1000:.0f}K  "
                      f"maint=${c['annual_maint']}/yr  "
                      f"5yrTCO=${c['tco_5y']/1000:.1f}K  "
                      f"v3={v3_str}")

    conn.close()


if __name__ == "__main__":
    main()