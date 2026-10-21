from typing import List, Dict, Any
from .database import get_connection, search_products

BGN_TO_EUR = 1 / 1.95583

def compare_basket(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Given a list of requested items, e.g.:
    [
        {"category": "Суроватъчен изолат", "preference": "cheapest"},
        {"category": "Креатин", "preference": "cheapest"}
    ]
    Calculates the total cost in EUR (and BGN) at each store,
    accounting for free shipping thresholds in EUR.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    stores = [dict(s) for s in cursor.fetchall()]
    conn.close()

    store_baskets = {}
    for s in stores:
        store_baskets[s["code"]] = {
            "store_info": s,
            "items": [],
            "missing_items": [],
            "subtotal_eur": 0.0,
            "subtotal_bgn": 0.0,
            "shipping_eur": 0.0,
            "shipping_bgn": 0.0,
            "total_eur": 0.0,
            "total_bgn": 0.0,
            "qualifies_free_shipping": False
        }

    for req in items:
        cat = req.get("category")
        brand = req.get("brand")

        for store in stores:
            store_code = store["code"]
            prods = search_products(category=cat, store_code=store_code, sort_by="price_eur_asc")
            if brand and brand != "any":
                prods = [p for p in prods if p["brand"] == brand] or prods

            if prods:
                best = prods[0]
                store_baskets[store_code]["items"].append(best)
                store_baskets[store_code]["subtotal_eur"] += best["price_eur"]
                store_baskets[store_code]["subtotal_bgn"] += best["price_bgn"]
            else:
                store_baskets[store_code]["missing_items"].append(cat)

    results = []
    for code, b in store_baskets.items():
        s_info = b["store_info"]
        subtotal_eur = round(b["subtotal_eur"], 2)
        subtotal_bgn = round(b["subtotal_bgn"], 2)

        # Free shipping threshold in EUR
        threshold_eur = s_info.get("free_shipping_threshold_eur") or round(s_info["free_shipping_threshold"] * BGN_TO_EUR, 2)
        shipping_eur_cost = s_info.get("standard_shipping_eur") or round(s_info["standard_shipping_bgn"] * BGN_TO_EUR, 2)

        if subtotal_eur >= threshold_eur:
            shipping_eur = 0.0
            shipping_bgn = 0.0
            qualifies = True
        elif subtotal_eur > 0:
            shipping_eur = shipping_eur_cost
            shipping_bgn = round(s_info["standard_shipping_bgn"], 2)
            qualifies = False
        else:
            shipping_eur = 0.0
            shipping_bgn = 0.0
            qualifies = False

        total_eur = round(subtotal_eur + shipping_eur, 2)
        total_bgn = round(subtotal_bgn + shipping_bgn, 2)

        b["subtotal"] = subtotal_bgn
        b["shipping"] = shipping_bgn
        b["total"] = total_bgn
        b["subtotal_eur"] = subtotal_eur
        b["shipping_eur"] = shipping_eur
        b["total_eur"] = total_eur
        b["qualifies_free_shipping"] = qualifies
        b["complete"] = len(b["missing_items"]) == 0 and len(b["items"]) == len(items)
        results.append(b)

    # Sort results: complete baskets first, then lowest total EUR
    results.sort(key=lambda x: (not x["complete"], x["total_eur"] if x["total_eur"] > 0 else 99999))

    best_single = results[0] if results and results[0]["complete"] else None

    # Calculate optimal split in EUR
    split_items = []
    split_subtotal_eur = 0.0
    split_subtotal_bgn = 0.0
    for req in items:
        cat = req.get("category")
        all_matches = search_products(category=cat, sort_by="price_eur_asc")
        if all_matches:
            cheapest = all_matches[0]
            split_items.append(cheapest)
            split_subtotal_eur += cheapest["price_eur"]
            split_subtotal_bgn += cheapest["price_bgn"]

    return {
        "requested_items": items,
        "store_comparisons": results,
        "best_single_store": best_single,
        "split_basket": {
            "items": split_items,
            "subtotal_eur": round(split_subtotal_eur, 2),
            "subtotal_bgn": round(split_subtotal_bgn, 2)
        }
    }
