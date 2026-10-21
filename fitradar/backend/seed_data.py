import os
from .database import init_db, upsert_store, upsert_product, DB_PATH
from .normalizer import normalize_product

STORES_DATA = [
    {
        "code": "decathlon",
        "name": "Декатлон (Decathlon BG)",
        "base_url": "https://www.decathlon.bg",
        "free_shipping_threshold": 100.0,
        "standard_shipping_bgn": 4.90,
        "badge_color": "#0288D1"
    },
    {
        "code": "silabg",
        "name": "Сила БГ (SilaBG)",
        "base_url": "https://www.silabg.com",
        "free_shipping_threshold": 70.0,
        "standard_shipping_bgn": 5.90,
        "badge_color": "#D32F2F"
    },
    {
        "code": "workoutbg",
        "name": "Workout.bg",
        "base_url": "https://workout.bg",
        "free_shipping_threshold": 60.0,
        "standard_shipping_bgn": 5.50,
        "badge_color": "#1976D2"
    },
    {
        "code": "gymbeam",
        "name": "GymBeam България",
        "base_url": "https://gymbeam.bg",
        "free_shipping_threshold": 80.0,
        "standard_shipping_bgn": 6.90,
        "badge_color": "#FF6F00"
    },
    {
        "code": "fitnes1",
        "name": "Фитнес 1 (Fitnes1.bg)",
        "base_url": "https://fitnes1.bg",
        "free_shipping_threshold": 65.0,
        "standard_shipping_bgn": 5.00,
        "badge_color": "#388E3C"
    },
    {
        "code": "myprotein",
        "name": "MyProtein България",
        "base_url": "https://www.myprotein.bg",
        "free_shipping_threshold": 90.0,
        "standard_shipping_bgn": 7.90,
        "badge_color": "#00838F"
    }
]

RAW_SAMPLE_PRODUCTS = [
    # ==================== DECATHLON BULGARIA ====================
    {
        "store_code": "decathlon",
        "external_id": "dec-001",
        "raw_title": "Суроватъчен протеин Whey шоколад 900 г Corength Decathlon",
        "price_bgn": 42.99,
        "old_price_bgn": 49.99,
        "flavor": "Шоколад",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-002",
        "raw_title": "Суроватъчен протеин Whey ванилия 900 г Corength Decathlon",
        "price_bgn": 42.99,
        "old_price_bgn": 49.99,
        "flavor": "Ванилия",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-003",
        "raw_title": "Суроватъчен протеин Whey бисквитки и сметана 900 г Corength",
        "price_bgn": 42.99,
        "old_price_bgn": 49.99,
        "flavor": "Бисквити и сметана",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-004",
        "raw_title": "Суроватъчен протеин Whey малка опаковка 450 г шоколад Corength",
        "price_bgn": 24.99,
        "old_price_bgn": 28.99,
        "flavor": "Шоколад",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-005",
        "raw_title": "Суроватъчен протеин изолат Pure Whey Isolate 900 г Шоколад Decathlon",
        "price_bgn": 59.99,
        "old_price_bgn": 69.99,
        "flavor": "Шоколад",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-006",
        "raw_title": "Суроватъчен протеин изолат Pure Whey Isolate 900 г Ванилия Decathlon",
        "price_bgn": 59.99,
        "old_price_bgn": 69.99,
        "flavor": "Ванилия",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-007",
        "raw_title": "Суроватъчен протеин изолат Pure Whey Isolate икономична 2 кг Шоколад",
        "price_bgn": 119.99,
        "old_price_bgn": 139.99,
        "flavor": "Шоколад",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-008",
        "raw_title": "Растителен протеин Vegan Protein 900 г Шоколад Decathlon Corength",
        "price_bgn": 46.99,
        "old_price_bgn": 54.99,
        "flavor": "Шоколад",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-009",
        "raw_title": "Креатин монохидрат Creapure® на прах 300 г Corength Decathlon",
        "price_bgn": 34.99,
        "old_price_bgn": 41.99,
        "flavor": "Без вкус",
        "product_url": "https://www.decathlon.bg/8466-kreatin",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-010",
        "raw_title": "Креатин монохидрат микронизиран прах 500 г Decathlon",
        "price_bgn": 32.99,
        "old_price_bgn": 39.99,
        "flavor": "Без вкус",
        "product_url": "https://www.decathlon.bg/8466-kreatin",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-011",
        "raw_title": "Предтренировъчен буустър Pre-Workout Booster 300 г Лимон Corength",
        "price_bgn": 39.99,
        "old_price_bgn": 47.99,
        "flavor": "Лимон",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-012",
        "raw_title": "Аминокиселини BCAA 4:1:1 на прах 300 г Праскова Decathlon Corength",
        "price_bgn": 29.99,
        "old_price_bgn": 35.99,
        "flavor": "Праскова",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-013",
        "raw_title": "Гейнър за маса Lean Mass Gainer 1.5 kg Шоколад Corength Decathlon",
        "price_bgn": 44.99,
        "old_price_bgn": 52.99,
        "flavor": "Шоколад",
        "product_url": "https://www.decathlon.bg/8424-geynari",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-014",
        "raw_title": "Изотонична напитка на прах Aptonia Iso Drink 650 г Портокал",
        "price_bgn": 18.99,
        "old_price_bgn": 22.99,
        "flavor": "Портокал",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "decathlon",
        "external_id": "dec-015",
        "raw_title": "Optimum Nutrition Gold Standard 100% Whey 908 гр Decathlon Partner",
        "price_bgn": 84.99,
        "old_price_bgn": 94.99,
        "flavor": "Double Rich Chocolate",
        "product_url": "https://www.decathlon.bg/7432-proteini-i-hranitelni-dobavki",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },

    # ==================== SILA BG ====================
    {
        "store_code": "silabg",
        "external_id": "sila-101",
        "raw_title": "Optimum Nutrition Gold Standard 100% Whey 2.27 kg - Двойно богат шоколад",
        "price_bgn": 154.90,
        "old_price_bgn": 189.90,
        "flavor": "Double Rich Chocolate",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Optimum+Nutrition+Gold+Standard+100%25+Whey",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-101b",
        "raw_title": "Optimum Nutrition Gold Standard 100% Whey 908 гр Ванилов сладолед",
        "price_bgn": 77.90,
        "old_price_bgn": 92.00,
        "flavor": "Vanilla Ice Cream",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Optimum+Nutrition+Gold+Standard+908",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-102",
        "raw_title": "BioTech USA Iso Whey Zero 2270 гр - Суроватъчен изолат без лактоза",
        "price_bgn": 146.00,
        "old_price_bgn": 178.00,
        "flavor": "Chocolate Toffee",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=BioTech+USA+Iso+Whey+Zero+2270",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-102b",
        "raw_title": "BioTech USA Iso Whey Zero 908 гр Ягода",
        "price_bgn": 68.90,
        "old_price_bgn": 84.00,
        "flavor": "Strawberry",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=BioTech+USA+Iso+Whey+Zero+908",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-103",
        "raw_title": "Scitec Nutrition 100% Whey Protein Professional 2350 гр",
        "price_bgn": 132.50,
        "old_price_bgn": 159.00,
        "flavor": "Chocolate Hazelnut",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Scitec+Nutrition+100%25+Whey+Professional",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-103b",
        "raw_title": "Scitec Nutrition 100% Whey Protein Professional 920 гр Банан",
        "price_bgn": 63.90,
        "old_price_bgn": 78.00,
        "flavor": "Banana",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Scitec+Nutrition+100%25+Whey+920",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-104",
        "raw_title": "Everbuild Nutrition Whey Build 2.0 / 2270 гр / 67 дози",
        "price_bgn": 109.90,
        "old_price_bgn": 139.90,
        "flavor": "Chocolate Brownie",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Everbuild+Whey+Build",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-105",
        "raw_title": "Everbuild Nutrition Iso Build 2270 гр Чист суроватъчен изолат",
        "price_bgn": 139.90,
        "old_price_bgn": 169.90,
        "flavor": "Chocolate",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Everbuild+Iso+Build",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-106",
        "raw_title": "Applied Nutrition Critical Whey 2000 гр Шоколадов шейк",
        "price_bgn": 114.90,
        "old_price_bgn": 139.00,
        "flavor": "Chocolate Shake",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Applied+Nutrition+Critical+Whey",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-201",
        "raw_title": "BioTech USA 100% Micronized Creatine Monohydrate 500 гр",
        "price_bgn": 39.90,
        "old_price_bgn": 49.90,
        "flavor": "Unflavored",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=BioTech+USA+Creatine+Monohydrate+500",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-202",
        "raw_title": "Everbuild Nutrition Pure Creatine Creapure 500 гр",
        "price_bgn": 49.90,
        "old_price_bgn": 62.00,
        "flavor": "Unflavored",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Everbuild+Creapure+500",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-301",
        "raw_title": "Applied Nutrition ABE All Black Everything Pre-Workout 315g / 30 дози",
        "price_bgn": 54.90,
        "old_price_bgn": 69.90,
        "flavor": "Energy Ice",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Applied+Nutrition+ABE",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-302",
        "raw_title": "Cellucor C4 Original Pre-Workout 390 гр 60 дози",
        "price_bgn": 79.90,
        "old_price_bgn": 99.00,
        "flavor": "Icy Blue Razz",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Cellucor+C4+Original+60",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-401",
        "raw_title": "Universal Nutrition Animal Pak / 44 пак мултивитаминен комплекс",
        "price_bgn": 79.90,
        "old_price_bgn": 98.00,
        "flavor": "Packs",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Universal+Animal+Pak",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-501",
        "raw_title": "Mutant Mass Gainer 6.8 kg Мега чувал за маса",
        "price_bgn": 129.90,
        "old_price_bgn": 159.00,
        "flavor": "Triple Chocolate",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Mutant+Mass+6.8",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "silabg",
        "external_id": "sila-601",
        "raw_title": "Everbuild Ultra Premium BCAA 8:1:1 400 гр Ягода и киви",
        "price_bgn": 44.90,
        "old_price_bgn": 55.00,
        "flavor": "Strawberry Kiwi",
        "product_url": "https://www.silabg.com/bg/search.html?keyword=Everbuild+BCAA+8:1:1",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },

    # ==================== WORKOUT.BG ====================
    {
        "store_code": "workoutbg",
        "external_id": "work-101",
        "raw_title": "OPTIMUM NUTRITION 100% Whey Gold Standard 2270g / 74 дози ТОП ПРОМОЦИЯ",
        "price_bgn": 149.00,
        "old_price_bgn": 179.00,
        "flavor": "Chocolate Mint",
        "product_url": "https://workout.bg/search.html?phrase=optimum+nutrition+gold+standard",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-101b",
        "raw_title": "OPTIMUM NUTRITION 100% Whey Gold Standard 908g Шоколад",
        "price_bgn": 75.90,
        "old_price_bgn": 89.90,
        "flavor": "Double Rich Chocolate",
        "product_url": "https://workout.bg/search.html?phrase=gold+standard+908",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-102",
        "raw_title": "BIOTECH USA Iso Whey Zero 2.27 kg ПРОМОЦИОНАЛЕН ПАКЕТ",
        "price_bgn": 139.99,
        "old_price_bgn": 169.90,
        "flavor": "Vanilla",
        "product_url": "https://workout.bg/search.html?phrase=biotech+iso+whey+zero",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-102b",
        "raw_title": "BIOTECH USA Iso Whey Zero 908g Шоколад",
        "price_bgn": 66.90,
        "old_price_bgn": 82.00,
        "flavor": "Chocolate",
        "product_url": "https://workout.bg/search.html?phrase=biotech+iso+whey+908",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-103",
        "raw_title": "SCITEC NUTRITION 100% Whey Professional 2.35 kg -20% НАМАЛЕНИЕ",
        "price_bgn": 128.90,
        "old_price_bgn": 162.00,
        "flavor": "Strawberry White Chocolate",
        "product_url": "https://workout.bg/search.html?phrase=scitec+100+whey",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-103b",
        "raw_title": "SCITEC NUTRITION 100% Whey Professional 920g Шоколад",
        "price_bgn": 61.90,
        "old_price_bgn": 75.00,
        "flavor": "Chocolate",
        "product_url": "https://workout.bg/search.html?phrase=scitec+whey+920",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-105",
        "raw_title": "Kevin Levrone Anabolic ISO Whey 2 kg Премиум чист изолат",
        "price_bgn": 134.99,
        "old_price_bgn": 165.00,
        "flavor": "Snickers",
        "product_url": "https://workout.bg/search.html?phrase=kevin+levrone+iso+whey",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-106",
        "raw_title": "Yamamoto Nutrition Iso-FUJI 2 kg Японско микрофилтрирано качество",
        "price_bgn": 149.99,
        "old_price_bgn": 179.00,
        "flavor": "Gourmet Chocolate",
        "product_url": "https://workout.bg/search.html?phrase=yamamoto+isofuji",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-201",
        "raw_title": "BIOTECH USA 100% Creatine Monohydrate 500g / 100 дози",
        "price_bgn": 34.90,
        "old_price_bgn": 45.00,
        "flavor": "Unflavored",
        "product_url": "https://workout.bg/search.html?phrase=biotech+creatine+monohydrate",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-202",
        "raw_title": "SCITEC NUTRITION 100% Creatine Monohydrate 500g Чист прах",
        "price_bgn": 36.90,
        "old_price_bgn": 46.00,
        "flavor": "Unflavored",
        "product_url": "https://workout.bg/search.html?phrase=scitec+creatine+500",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-301",
        "raw_title": "APPLIED NUTRITION ABE All Black Everything 315 гр ТОП ЦЕНА",
        "price_bgn": 49.90,
        "old_price_bgn": 65.00,
        "flavor": "Blue Raspberry",
        "product_url": "https://workout.bg/search.html?phrase=applied+nutrition+abe",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-302",
        "raw_title": "CELLUCOR C4 Original 30 servings 195g Плодов пунш",
        "price_bgn": 48.90,
        "old_price_bgn": 60.00,
        "flavor": "Fruit Punch",
        "product_url": "https://workout.bg/search.html?phrase=c4+original",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-401",
        "raw_title": "UNIVERSAL Animal Pak 44 packs Легендарни витамини",
        "price_bgn": 74.90,
        "old_price_bgn": 94.00,
        "flavor": "Packs",
        "product_url": "https://workout.bg/search.html?phrase=animal+pak",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-501",
        "raw_title": "APPLIED NUTRITION Critical Mass Gainer 2.4 kg Ванилия",
        "price_bgn": 64.90,
        "old_price_bgn": 79.90,
        "flavor": "Vanilla",
        "product_url": "https://workout.bg/search.html?phrase=critical+mass",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "workoutbg",
        "external_id": "work-601",
        "raw_title": "BSN Amino X Endurance & Recovery 435g Диня",
        "price_bgn": 47.90,
        "old_price_bgn": 59.90,
        "flavor": "Watermelon",
        "product_url": "https://workout.bg/search.html?phrase=bsn+amino+x",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },

    # ==================== GYMBEAM BULGARIA ====================
    {
        "store_code": "gymbeam",
        "external_id": "gym-101",
        "raw_title": "GymBeam Just Whey 1000g суроватъчен протеин от свободно пасящи крави",
        "price_bgn": 54.90,
        "old_price_bgn": 64.90,
        "flavor": "Chocolate Milkshake",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=just+whey",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-101b",
        "raw_title": "GymBeam Just Whey 1000g Ванилов сладолед",
        "price_bgn": 54.90,
        "old_price_bgn": 64.90,
        "flavor": "Vanilla",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=just+whey+vanilla",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-102",
        "raw_title": "GymBeam Just Whey 2000g икономична разфасовка",
        "price_bgn": 94.90,
        "old_price_bgn": 114.90,
        "flavor": "Salted Caramel",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=just+whey+2000g",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-103",
        "raw_title": "GymBeam IsoFue 1000g чист суроватъчен изолат без лактоза",
        "price_bgn": 69.90,
        "old_price_bgn": 84.90,
        "flavor": "Chocolate",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=isofue",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-104",
        "raw_title": "GymBeam IsoFue 2000g суроватъчен изолат голяма кутия",
        "price_bgn": 129.90,
        "old_price_bgn": 154.90,
        "flavor": "Vanilla",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=isofue+2000g",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-105",
        "raw_title": "GymBeam True Whey 1000g чист WPC суроватъчен концентрат",
        "price_bgn": 49.90,
        "old_price_bgn": 59.90,
        "flavor": "White Chocolate",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=true+whey",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-106",
        "raw_title": "GymBeam True Whey 2500g семейна разфасовка",
        "price_bgn": 104.90,
        "old_price_bgn": 129.90,
        "flavor": "Chocolate Hazelnut",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=true+whey+2500g",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-107",
        "raw_title": "GymBeam Vegan Blend 1000g растителен протеин Шоколад",
        "price_bgn": 46.90,
        "old_price_bgn": 56.90,
        "flavor": "Chocolate",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=vegan+blend",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-201",
        "raw_title": "GymBeam Креатин Монохидрат 100% чист прах 500 гр",
        "price_bgn": 29.90,
        "old_price_bgn": 38.90,
        "flavor": "Unflavored",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=creatine+monohydrate",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-202",
        "raw_title": "GymBeam 100% Creapure® Креатин Монохидрат 500 гр",
        "price_bgn": 42.90,
        "old_price_bgn": 52.90,
        "flavor": "Unflavored",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=creapure",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-301",
        "raw_title": "GymBeam Thor предтренировъчен буустър 210g Диня",
        "price_bgn": 34.90,
        "old_price_bgn": 42.90,
        "flavor": "Watermelon",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=thor+preworkout",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-401",
        "raw_title": "GymBeam Daily Vitamin Complex 120 капсули",
        "price_bgn": 17.90,
        "old_price_bgn": 22.90,
        "flavor": "Capsules",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=daily+vitamin",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-501",
        "raw_title": "GymBeam FueGain All-in-One Mass Gainer 2.5 kg Шоколад",
        "price_bgn": 74.90,
        "old_price_bgn": 89.90,
        "flavor": "Chocolate",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=fuegain",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "gymbeam",
        "external_id": "gym-601",
        "raw_title": "GymBeam BCAA 4:1:1 Instant 500g Зелена ябълка",
        "price_bgn": 37.90,
        "old_price_bgn": 46.90,
        "flavor": "Green Apple",
        "product_url": "https://gymbeam.bg/catalogsearch/result/?q=bcaa+411",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },

    # ==================== FITNES 1 (FITNES1.BG) ====================
    {
        "store_code": "fitnes1",
        "external_id": "fit1-101",
        "raw_title": "Optimum Nutrition Gold Standard 100% Whey Protein 908 гр",
        "price_bgn": 79.90,
        "old_price_bgn": 92.00,
        "flavor": "Vanilla Ice Cream",
        "product_url": "https://fitnes1.bg/?s=gold+standard+908&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-101b",
        "raw_title": "Optimum Nutrition Gold Standard 100% Whey 2270 гр Двоен шоколад",
        "price_bgn": 155.90,
        "old_price_bgn": 185.00,
        "flavor": "Double Rich Chocolate",
        "product_url": "https://fitnes1.bg/?s=gold+standard+2270&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-102",
        "raw_title": "BioTech USA Iso Whey Zero 908g / 36 дози",
        "price_bgn": 69.90,
        "old_price_bgn": 84.00,
        "flavor": "Cookies and Cream",
        "product_url": "https://fitnes1.bg/?s=iso+whey+zero+908&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-102b",
        "raw_title": "BioTech USA Iso Whey Zero 2270g Ванилия",
        "price_bgn": 144.00,
        "old_price_bgn": 175.00,
        "flavor": "Vanilla",
        "product_url": "https://fitnes1.bg/?s=iso+whey+zero+2270&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-103",
        "raw_title": "Scitec Nutrition 100% Whey Protein Professional 1000g Шоколад",
        "price_bgn": 66.90,
        "old_price_bgn": 79.90,
        "flavor": "Chocolate",
        "product_url": "https://fitnes1.bg/?s=scitec+whey+1000&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-104",
        "raw_title": "Dymatize ISO 100 Hydrolyzed Whey Isolate 2200g Гурме шоколад",
        "price_bgn": 169.90,
        "old_price_bgn": 205.00,
        "flavor": "Gourmet Chocolate",
        "product_url": "https://fitnes1.bg/?s=dymatize+iso+100&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-105",
        "raw_title": "Olimp Whey Protein Complex 100% 700g Ягода",
        "price_bgn": 49.90,
        "old_price_bgn": 59.90,
        "flavor": "Strawberry",
        "product_url": "https://fitnes1.bg/?s=olimp+whey+700&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-201",
        "raw_title": "Everbuild Nutrition 100% Pure Micropure Creapure Creatine 300g",
        "price_bgn": 36.90,
        "old_price_bgn": 46.00,
        "flavor": "Unflavored",
        "product_url": "https://fitnes1.bg/?s=creapure&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-202",
        "raw_title": "Everbuild Nutrition Pure Micronized Creatine 500g",
        "price_bgn": 38.90,
        "old_price_bgn": 48.00,
        "flavor": "Unflavored",
        "product_url": "https://fitnes1.bg/?s=everbuild+creatine+500&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-301",
        "raw_title": "Cellucor C4 Original Pre-Workout 30 дози / 195g",
        "price_bgn": 52.00,
        "old_price_bgn": 62.00,
        "flavor": "Fruit Punch",
        "product_url": "https://fitnes1.bg/?s=c4+original&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-302",
        "raw_title": "BioTech USA Black Blood NOX+ екстремен буустър 330g",
        "price_bgn": 57.90,
        "old_price_bgn": 69.90,
        "flavor": "Blue Grape",
        "product_url": "https://fitnes1.bg/?s=black+blood&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-401",
        "raw_title": "Universal Nutrition Animal Pak 44 пак",
        "price_bgn": 79.90,
        "old_price_bgn": 99.00,
        "flavor": "Packs",
        "product_url": "https://fitnes1.bg/?s=animal+pak&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-501",
        "raw_title": "BSN True Mass 1200 Mega Gainer 4.7 kg Шоколад",
        "price_bgn": 119.90,
        "old_price_bgn": 145.00,
        "flavor": "Chocolate",
        "product_url": "https://fitnes1.bg/?s=true+mass&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "fitnes1",
        "external_id": "fit1-601",
        "raw_title": "Scitec Nutrition BCAA Xpress 700g Манго",
        "price_bgn": 54.90,
        "old_price_bgn": 67.00,
        "flavor": "Mango",
        "product_url": "https://fitnes1.bg/?s=bcaa+xpress&post_type=product",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },

    # ==================== MYPROTEIN BULGARIA ====================
    {
        "store_code": "myprotein",
        "external_id": "mp-100",
        "raw_title": "MyProtein Impact Whey Protein 1000g Chocolate Smooth",
        "price_bgn": 53.90,
        "old_price_bgn": 75.00,
        "flavor": "Chocolate Smooth",
        "product_url": "https://www.myprotein.bg/elysium.search?search=impact+whey+protein",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-100b",
        "raw_title": "MyProtein Impact Whey Protein 2500g Vanilla",
        "price_bgn": 109.90,
        "old_price_bgn": 155.00,
        "flavor": "Vanilla",
        "product_url": "https://www.myprotein.bg/elysium.search?search=impact+whey+protein+2.5kg",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-100c",
        "raw_title": "MyProtein Impact Whey Protein 5000g икономичен чувал",
        "price_bgn": 195.00,
        "old_price_bgn": 280.00,
        "flavor": "Natural Chocolate",
        "product_url": "https://www.myprotein.bg/elysium.search?search=impact+whey+protein+5kg",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-101",
        "raw_title": "MyProtein Impact Whey Isolate 1000g (Чист суроватъчен изолат)",
        "price_bgn": 69.90,
        "old_price_bgn": 99.90,
        "flavor": "Natural Chocolate",
        "product_url": "https://www.myprotein.bg/elysium.search?search=impact+whey+isolate",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-102",
        "raw_title": "MyProtein Impact Whey Isolate 2.5 kg / 100 дози",
        "price_bgn": 149.00,
        "old_price_bgn": 215.00,
        "flavor": "Vanilla",
        "product_url": "https://www.myprotein.bg/elysium.search?search=impact+whey+isolate+2500g",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-103",
        "raw_title": "MyProtein Clear Whey Isolate 500g Orange Mango (Бистър протеин)",
        "price_bgn": 64.90,
        "old_price_bgn": 89.90,
        "flavor": "Orange Mango",
        "product_url": "https://www.myprotein.bg/elysium.search?search=clear+whey+isolate",
        "image_url": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-201",
        "raw_title": "MyProtein Creatine Monohydrate микронизиран прах 500g",
        "price_bgn": 31.90,
        "old_price_bgn": 44.90,
        "flavor": "Unflavored",
        "product_url": "https://www.myprotein.bg/elysium.search?search=creatine+monohydrate",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-202",
        "raw_title": "MyProtein Creapure® Creatine Monohydrate 250g Чист креатин",
        "price_bgn": 37.90,
        "old_price_bgn": 49.90,
        "flavor": "Unflavored",
        "product_url": "https://www.myprotein.bg/elysium.search?search=creapure",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-301",
        "raw_title": "MyProtein The Pre-Workout 30 дози Синя малина",
        "price_bgn": 54.90,
        "old_price_bgn": 72.00,
        "flavor": "Blue Raspberry",
        "product_url": "https://www.myprotein.bg/elysium.search?search=the+pre+workout",
        "image_url": "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-401",
        "raw_title": "MyProtein Daily Multivitamin 180 таблетки за 6 месеца",
        "price_bgn": 24.90,
        "old_price_bgn": 34.90,
        "flavor": "Tablets",
        "product_url": "https://www.myprotein.bg/elysium.search?search=daily+multivitamin",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-501",
        "raw_title": "MyProtein Weight Gainer Blend 2.5 kg Шоколад",
        "price_bgn": 59.90,
        "old_price_bgn": 84.90,
        "flavor": "Chocolate",
        "product_url": "https://www.myprotein.bg/elysium.search?search=weight+gainer+blend",
        "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=400&auto=format&fit=crop&q=60"
    },
    {
        "store_code": "myprotein",
        "external_id": "mp-601",
        "raw_title": "MyProtein Essential BCAA 500g Горски плодове",
        "price_bgn": 44.90,
        "old_price_bgn": 59.90,
        "flavor": "Berry Burst",
        "product_url": "https://www.myprotein.bg/elysium.search?search=essential+bcaa",
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&auto=format&fit=crop&q=60"
    }
]

def seed():
    # Remove existing db file if we want clean fresh seed
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    print("[FitRadar BG] Initializing database...")
    init_db()

    print("[FitRadar BG] Seeding Bulgarian retailers...")
    for s in STORES_DATA:
        upsert_store(
            code=s["code"],
            name=s["name"],
            base_url=s["base_url"],
            free_shipping_threshold=s["free_shipping_threshold"],
            standard_shipping_bgn=s["standard_shipping_bgn"],
            badge_color=s["badge_color"]
        )

    print("[FitRadar BG] Normalizing and inserting products...")
    for p in RAW_SAMPLE_PRODUCTS:
        norm = normalize_product(p)
        upsert_product(norm)

    print(f"[FitRadar BG] Successfully seeded {len(RAW_SAMPLE_PRODUCTS)} products across {len(STORES_DATA)} stores!")

if __name__ == "__main__":
    seed()
