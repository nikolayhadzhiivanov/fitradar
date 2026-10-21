import re
from typing import Dict, Any, Tuple, Optional

KNOWN_BRANDS = [
    "Optimum Nutrition", "BioTech USA", "Scitec Nutrition", "Everbuild",
    "GymBeam", "MyProtein", "Applied Nutrition", "Amix Nutrition",
    "BSN", "Kevin Levrone", "Yamamoto Nutrition", "Reflex Nutrition",
    "Dymatize", "Universal Nutrition", "Mutant", "Rule 1", "Olimp",
    "Decathlon (Corength)", "Quamtrax", "Weider"
]

BGN_TO_EUR = 1 / 1.95583

def clean_text(text: str) -> str:
    if not text:
        return ""
    # Normalize unicode whitespace and lowercase
    t = text.strip()
    t = re.sub(r'\s+', ' ', t)
    return t

def extract_weight_and_servings(title: str, form: str = "powder") -> Tuple[Optional[float], Optional[int]]:
    """
    Extracts net weight in grams and estimated servings from product title.
    Returns (weight_g, servings).
    """
    weight_g = None
    servings = None

    # Check for kg (e.g. 2.27 kg, 2,27кг, 1kg)
    kg_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:kg|кг)\b', title, re.IGNORECASE)
    if kg_match:
        weight_g = float(kg_match.group(1).replace(',', '.')) * 1000.0

    # Check for grams (e.g. 2270 g, 2270гр, 908g, 500 гр, 900 г, 300 грама)
    if not weight_g:
        g_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:g|гр|грама|gr|г)(?:\b|[^\w]|$)', title, re.IGNORECASE)
        if g_match:
            weight_g = float(g_match.group(1).replace(',', '.'))

    # Check for lbs (e.g. 5 lbs, 2 lb)
    if not weight_g:
        lbs_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:lbs?|либри)\b', title, re.IGNORECASE)
        if lbs_match:
            weight_g = float(lbs_match.group(1).replace(',', '.')) * 453.592

    # Check for servings / capsules / tablets
    caps_match = re.search(r'(\d+)\s*(?:капсули|капс|caps|capsules|tabs|таблетки|дози|servings|дражета|пак|packs)\b', title, re.IGNORECASE)
    if caps_match:
        servings = int(caps_match.group(1))

    # If powder and weight is known but servings unknown, estimate servings (~30g per scoop for protein, ~5g for creatine)
    if weight_g and not servings:
        if "креатин" in title.lower() or "creatine" in title.lower():
            servings = int(weight_g / 5.0)
        elif "протеин" in title.lower() or "protein" in title.lower() or "whey" in title.lower():
            servings = int(weight_g / 30.0)

    return (round(weight_g, 1) if weight_g else None, servings)

def detect_brand(title: str) -> str:
    title_lower = title.lower()
    for brand in KNOWN_BRANDS:
        if brand.lower() in title_lower:
            return brand

    # Specific brand aliases
    if "on " in title_lower or "gold standard" in title_lower:
        return "Optimum Nutrition"
    if "biotech" in title_lower or "iso whey zero" in title_lower:
        return "BioTech USA"
    if "scitec" in title_lower:
        return "Scitec Nutrition"
    if "everbuild" in title_lower:
        return "Everbuild"
    if "applied" in title_lower:
        return "Applied Nutrition"
    if "amix" in title_lower:
        return "Amix Nutrition"
    if "animal" in title_lower:
        return "Universal Nutrition"
    if "gymbeam" in title_lower:
        return "GymBeam"
    if "myprotein" in title_lower:
        return "MyProtein"
    if "corength" in title_lower or "decathlon" in title_lower or "aptonia" in title_lower:
        return "Decathlon (Corength)"
    if "quamtrax" in title_lower:
        return "Quamtrax"
    if "weider" in title_lower:
        return "Weider"

    return "Други марки"

def detect_category(title: str) -> str:
    tl = title.lower()
    if any(k in tl for k in ["изолат", "isolate", "iso whey", "zero"]):
        return "Суроватъчен изолат"
    if any(k in tl for k in ["хидролизат", "hydro", "hydrolyzed"]):
        return "Суроватъчен хидролизат"
    if any(k in tl for k in ["гейнър", "gainer", "mass"]):
        return "Гейнър за маса"
    if any(k in tl for k in ["whey", "суроватъчен", "протеин", "protein"]):
        return "Суроватъчен концентрат"
    if any(k in tl for k in ["креатин", "creatine", "creapure"]):
        return "Креатин"
    if any(k in tl for k in ["pre-workout", "буустър", "бустер", "c4", "abe", "pump"]):
        return "Предтренировъчни"
    if any(k in tl for k in ["bcaa", "аминокиселини", "eaa", "amino"]):
        return "Аминокиселини (BCAA)"
    if any(k in tl for k in ["витамини", "мултивитамини", "vitamin", "omega", "омега", "mineral"]):
        return "Витамини и минерали"
    return "Хранителни добавки"

def estimate_protein_percentage(title: str, category: str) -> Optional[float]:
    tl = title.lower()
    if category == "Суроватъчен изолат":
        return 88.0
    if category == "Суроватъчен хидролизат":
        return 86.0
    if category == "Суроватъчен концентрат":
        # check specific brands
        if "gold standard" in tl:
            return 78.0
        return 74.0
    if category == "Гейнър за маса":
        return 22.0
    return None

def normalize_product(raw_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes raw scraped product dict and returns a normalized record ready for FitRadar database.
    """
    raw_title = clean_text(raw_dict.get("raw_title", ""))
    brand = raw_dict.get("brand") or detect_brand(raw_title)
    category = raw_dict.get("category") or detect_category(raw_title)
    form = raw_dict.get("form", "powder")
    flavor = raw_dict.get("flavor", "Неуточнен")

    weight_g, servings = extract_weight_and_servings(raw_title, form)
    if "weight_g" in raw_dict and raw_dict["weight_g"]:
        weight_g = float(raw_dict["weight_g"])
    if "servings" in raw_dict and raw_dict["servings"]:
        servings = int(raw_dict["servings"])

    protein_pct = raw_dict.get("protein_pct") or estimate_protein_percentage(raw_title, category)

    price_bgn = float(raw_dict.get("price_bgn", 0.0))
    old_price_bgn = float(raw_dict.get("old_price_bgn", 0.0)) if raw_dict.get("old_price_bgn") else None

    # Calculate EUR prices
    price_eur = round(price_bgn * BGN_TO_EUR, 2)
    old_price_eur = round(old_price_bgn * BGN_TO_EUR, 2) if old_price_bgn else None

    # Calculate discount percentage
    discount_pct = 0
    if old_price_bgn and old_price_bgn > price_bgn:
        discount_pct = int(round(((old_price_bgn - price_bgn) / old_price_bgn) * 100))

    # Calculate price per 100g
    price_per_100g = None
    price_per_100g_eur = None
    if weight_g and weight_g > 0 and price_bgn > 0:
        price_per_100g = round((price_bgn / weight_g) * 100.0, 2)
        price_per_100g_eur = round(price_per_100g * BGN_TO_EUR, 2)

    # Calculate price per serving
    price_per_serving = None
    price_per_serving_eur = None
    if servings and servings > 0 and price_bgn > 0:
        price_per_serving = round(price_bgn / servings, 2)
        price_per_serving_eur = round(price_per_serving * BGN_TO_EUR, 2)

    # Calculate price per 100g pure protein
    price_per_100g_protein = None
    if price_per_100g and protein_pct and protein_pct > 0:
        price_per_100g_protein = round((price_per_100g / (protein_pct / 100.0)), 2)

    # Simplified clean title (e.g. without messy promo codes and retailer slogans)
    clean_title = re.sub(r'(\s*-\s*\d+%\s*|\s*ТОП ЦЕНА\s*|\s*ПРОМОЦИЯ\s*|\s*БЕЗПЛАТНА ДОСТАВКА\s*)', '', raw_title, flags=re.IGNORECASE).strip()

    return {
        "store_code": raw_dict.get("store_code", "unknown"),
        "external_id": str(raw_dict.get("external_id", "")),
        "raw_title": raw_title,
        "clean_title": clean_title,
        "brand": brand,
        "category": category,
        "form": form,
        "flavor": flavor,
        "weight_g": weight_g,
        "servings": servings,
        "protein_pct": protein_pct,
        "price_bgn": round(price_bgn, 2),
        "old_price_bgn": round(old_price_bgn, 2) if old_price_bgn else None,
        "price_eur": price_eur,
        "old_price_eur": old_price_eur,
        "discount_pct": discount_pct,
        "price_per_100g": price_per_100g,
        "price_per_100g_eur": price_per_100g_eur,
        "price_per_100g_protein": price_per_100g_protein,
        "price_per_serving": price_per_serving,
        "price_per_serving_eur": price_per_serving_eur,
        "in_stock": int(raw_dict.get("in_stock", 1)),
        "product_url": raw_dict.get("product_url", "#"),
        "image_url": raw_dict.get("image_url", "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=400&auto=format&fit=crop&q=60")
    }
