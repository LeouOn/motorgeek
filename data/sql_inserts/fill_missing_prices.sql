-- Fill missing market prices for high-priority and bottom-buyer cars
-- All prices sourced from KBB, Cars.com, AutoTempest, BaT (2025-2026 market)

INSERT INTO market_history (car_id, date_recorded, price_low, price_high, source_site, currency, market_trend_indicator)
VALUES
-- ---- HIGH PRIORITY (user's cars of interest) ----
(43,  '2026-06-01', 35000, 50000, 'KBB/Cars.com 2026', 'USD', 'depreciating'),  -- Audi A8 D5 facelift
(132, '2026-06-01', 8000,  15000, 'AutoTempest 2026', 'USD', 'depreciating'),   -- VW Touareg 1 (7L)
(133, '2026-06-01', 14000, 22000, 'AutoTempest 2026', 'USD', 'depreciating'),   -- VW Touareg 2 (7P)
(134, '2026-06-01', 25000, 35000, 'Cars.com 2026', 'USD', 'stable'),           -- VW Touareg 3 (CR)
(164, '2026-06-01', 25000, 38000, 'KBB 2026', 'USD', 'depreciating'),          -- BMW 740i B58 G11/G12
(170, '2026-06-01', 35000, 50000, 'BaT/Cars.com 2026', 'USD', 'rising'),       -- Chevy SS LS3 6MT
(176, '2026-06-01', 12000, 20000, 'Hagerty 2026', 'USD', 'rising'),            -- BMW 740i E38
(178, '2026-06-01', 15000, 30000, 'Hagerty 2026', 'USD', 'rising'),            -- MB 560SEL W126
(179, '2026-06-01', 15000, 25000, 'KBB 2026', 'USD', 'depreciating'),          -- MB S550 W221

-- ---- BOTTOM BUYER SWEET SPOT ----
(86,  '2026-06-01', 10000, 16000, 'KBB 2026', 'USD', 'stable'),               -- Lexus ES 350 XV40
(165, '2026-06-01', 18000, 25000, 'KBB 2026', 'USD', 'depreciating'),          -- Lincoln Continental 3.0T
(166, '2026-06-01', 15000, 22000, 'KBB 2026', 'USD', 'depreciating'),          -- Chrysler 300 5.7L
(167, '2026-06-01', 16000, 24000, 'KBB 2026', 'USD', 'depreciating'),          -- Lincoln MKZ 3.0T
(168, '2026-06-01', 14000, 20000, 'KBB 2026', 'USD', 'depreciating'),          -- Buick LaCrosse 3.6L
(169, '2026-06-01', 15000, 22000, 'KBB 2026', 'USD', 'depreciating'),          -- Cadillac ATS 3.6L
(185, '2026-06-01', 22000, 30000, 'KBB 2026', 'USD', 'stable'),               -- Honda Accord 2.0T 6MT
(186, '2026-06-01', 10000, 16000, 'KBB 2026', 'USD', 'depreciating'),          -- Honda Accord Sport 6MT
(194, '2026-06-01', 18000, 30000, 'KBB 2026', 'USD', 'depreciating'),          -- Honda Odyssey EX-L
(198, '2026-06-01', 18000, 28000, 'KBB 2026', 'USD', 'stable'),               -- Toyota 4Runner SR5
(199, '2026-06-01', 15000, 22000, 'KBB 2026', 'USD', 'depreciating'),          -- Lexus RX350 3rd gen
(200, '2026-06-01', 18000, 28000, 'KBB 2026', 'USD', 'stable'),               -- Toyota Tundra SR5
(192, '2026-06-01', 12000, 20000, 'KBB 2026', 'USD', 'depreciating'),          -- Toyota Sienna XLE V6
(193, '2026-06-01', 30000, 45000, 'KBB 2026', 'USD', 'depreciating'),          -- Toyota Sienna Hybrid
(190, '2026-06-01', 12000, 18000, 'KBB 2026', 'USD', 'depreciating'),          -- Toyota Avalon XLE V6
(191, '2026-06-01', 13000, 19000, 'KBB 2026', 'USD', 'depreciating'),          -- Toyota Avalon Hybrid
(183, '2026-06-01', 10000, 15000, 'KBB 2026', 'USD', 'depreciating'),          -- Toyota Camry XSE V6
(184, '2026-06-01', 10000, 15000, 'KBB 2026', 'USD', 'depreciating'),          -- Toyota Camry Hybrid

-- ---- GERMAN INTEREST ----
(37,  '2026-06-01', 10000, 18000, 'KBB 2026', 'USD', 'rising'),               -- BMW E90 328i N52
(65,  '2026-06-01', 25000, 40000, 'Hagerty 2026', 'USD', 'rising'),            -- BMW M5 E39
(177, '2026-06-01', 8000,  14000, 'KBB 2026', 'USD', 'depreciating'),          -- Audi A8 D3 4.2
(180, '2026-06-01', 15000, 25000, 'KBB 2026', 'USD', 'depreciating'),          -- Audi A8 D4 3.0T

-- ---- JAPANESE INTEREST ----
(38,  '2026-06-01', 20000, 32000, 'KBB 2026', 'USD', 'depreciating'),          -- Genesis G70
(131, '2026-06-01', 18000, 28000, 'KBB 2026', 'USD', 'stable'),               -- Subaru BRZ
(187, '2026-06-01', 8000,  14000, 'KBB 2026', 'USD', 'depreciating'),          -- Mazda3 2.5L 6MT
(162, '2026-06-01', 22000, 30000, 'KBB 2026', 'USD', 'depreciating'),          -- Kia K5 GT
(197, '2026-06-01', 25000, 35000, 'KBB 2026', 'USD', 'depreciating'),          -- Kia Carnival

-- ---- MUSCLE / AMERICAN ----
(27,  '2026-06-01', 38000, 50000, 'KBB 2026', 'USD', 'depreciating'),          -- Cadillac CT5
(69,  '2026-06-01', 25000, 40000, 'Hagerty 2026', 'USD', 'rising'),            -- Cadillac CTS-V Gen1
(195, '2026-06-01', 18000, 28000, 'KBB 2026', 'USD', 'depreciating'),          -- Chrysler Pacifica
(85,  '2026-06-01', 14000, 20000, 'KBB 2026', 'USD', 'depreciating'),          -- Chevy Malibu Hybrid
(171, '2026-06-01', 35000, 50000, 'KBB 2026', 'USD', 'depreciating'),          -- Lincoln Navigator
(175, '2026-06-01', 35000, 55000, 'KBB 2026', 'USD', 'depreciating');          -- Cadillac Escalade
