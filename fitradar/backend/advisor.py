import re
from typing import Dict, Any, List
from .database import search_products

BGN_TO_EUR = 1 / 1.95583

def parse_user_intent(query: str) -> Dict[str, Any]:
    q = query.lower()
    intent = {
        "raw_query": query,
        "category": None,
        "max_price_eur": None,
        "brand": None,
        "sort_by": "price_per_100g_eur_asc",
        "focus": "value"
    }

    # Category matching
    if any(k in q for k in ["изолат", "isolate", "чист протеин", "без лактоза"]):
        intent["category"] = "Суроватъчен изолат"
    elif any(k in q for k in ["концентрат", "whey", "суроватъчен", "протеин", "protein"]):
        intent["category"] = "Суроватъчен концентрат"
    elif any(k in q for k in ["креатин", "creatine", "creapure"]):
        intent["category"] = "Креатин"
    elif any(k in q for k in ["буустър", "бустер", "pre-workout", "предтренировъч"]):
        intent["category"] = "Предтренировъчни"
    elif any(k in q for k in ["витамини", "мултивитамини", "animal pak", "минерали"]):
        intent["category"] = "Витамини и минерали"

    # Price constraints in EUR (e.g. "под 40 евро", "до 50€", "под 50 eur")
    eur_match = re.search(r'(?:под|до|максимум|до\s*към)\s*(\d+(?:[.,]\d+)?)\s*(?:евро|eur|€)', q)
    if eur_match:
        intent["max_price_eur"] = float(eur_match.group(1).replace(',', '.'))
    else:
        # Check BGN constraints (e.g. "под 70 лв") and convert to EUR
        bgn_match = re.search(r'(?:под|до|максимум|до\s*към)\s*(\d+(?:[.,]\d+)?)\s*(?:лв|лева|bgn)?', q)
        if bgn_match:
            bgn_val = float(bgn_match.group(1).replace(',', '.'))
            intent["max_price_eur"] = round(bgn_val * BGN_TO_EUR, 2)

    # Focus / Sorting criteria
    if any(k in q for k in ["най-евтин", "бюджетен", "евтина", "най-ниска цена"]):
        intent["sort_by"] = "price_eur_asc"
        intent["focus"] = "budget"
    elif any(k in q for k in ["намаление", "промоция", "отстъпка", "сделка"]):
        intent["sort_by"] = "discount_desc"
        intent["focus"] = "discount"
    elif any(k in q for k in ["процент", "чист", "качество", "висок процент"]):
        intent["sort_by"] = "protein_desc"
        intent["focus"] = "quality"
    else:
        intent["sort_by"] = "price_per_100g_eur_asc"
        intent["focus"] = "value_per_gram"

    return intent

def advise(query: str) -> Dict[str, Any]:
    intent = parse_user_intent(query)
    category = intent["category"]
    sort_by = intent["sort_by"]

    # Query products from database
    results = search_products(category=category, sort_by=sort_by)

    # Filter by budget in EUR if specified
    if intent["max_price_eur"]:
        results = [p for p in results if p.get("price_eur", 9999) <= intent["max_price_eur"]]

    if not results:
        results = search_products(query=query.split()[0] if query.split() else None, sort_by="price_per_100g_eur_asc")

    top_picks = results[:4]

    cat_label = category if category else "продукти"
    if intent["focus"] == "budget":
        advice_summary = f"Анализирах актуалните цени в евро за {cat_label}. Ето най-бюджетните оферти в момента на пазара:"
    elif intent["focus"] == "discount":
        advice_summary = f"Ето продуктите в категория {cat_label} с най-висок реален процент намаление спрямо стандартните им цени:"
    elif intent["focus"] == "quality":
        advice_summary = f"Подбрах предложения за {cat_label} с най-висока чистота и концентрация на активната съставка за доза:"
    else:
        advice_summary = f"Сравних цените на 100g активно вещество в евро (€) за {cat_label}. Ето най-изгодните покупки:"

    if top_picks:
        best = top_picks[0]
        price_eur_val = best.get('price_eur', round(best['price_bgn'] * BGN_TO_EUR, 2))
        price_100g_eur_val = best.get('price_per_100g_eur', round((best['price_per_100g'] or 0) * BGN_TO_EUR, 2))
        recommendation_text = (
            f"Препоръчваме **{best['clean_title']}** от магазин **{best['store_name']}** на цена от **€{price_eur_val:.2f}** "
            f"(Цена за 100g: **€{price_100g_eur_val:.2f}**, Спестяване: **{best['discount_pct']}%**)."
        )
    else:
        recommendation_text = "Не открихме точни съвпадения за зададените филтри, но разгледайте най-близките алтернативи по-долу."

    return {
        "intent": intent,
        "summary": advice_summary,
        "recommendation": recommendation_text,
        "products": top_picks
    }
