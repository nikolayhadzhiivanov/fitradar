import os
import sys

# Ensure parent directory is in sys.path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from flask import Flask, jsonify, request, send_from_directory
from backend.database import search_products, get_all_stores, get_categories_and_brands
from backend.basket import compare_basket
from backend.advisor import advise
from backend.seed_data import seed

app = Flask(__name__, static_folder="static", static_url_path="")

# Ensure database exists and is populated
DB_PATH = os.path.join(os.path.dirname(__file__), "backend", "fitradar.db")
if not os.path.exists(DB_PATH):
    seed()

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    target = os.path.join(app.static_folder, filename)
    if os.path.isfile(target):
        return send_from_directory(app.static_folder, filename)
    return jsonify({"error": "File not found"}), 404

@app.route("/api/products", methods=["GET"])
def api_products():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "all")
    store = request.args.get("store", "all")
    brand = request.args.get("brand", "all")
    sort_by = request.args.get("sort_by", "price_per_100g_asc")

    products = search_products(
        query=query if query else None,
        category=category,
        store_code=store,
        brand=brand,
        sort_by=sort_by
    )
    return jsonify({
        "status": "success",
        "total": len(products),
        "products": products
    })

@app.route("/api/meta", methods=["GET"])
def api_meta():
    stores = get_all_stores()
    cat_brands = get_categories_and_brands()
    return jsonify({
        "stores": stores,
        "categories": cat_brands["categories"],
        "brands": cat_brands["brands"]
    })

@app.route("/api/basket/compare", methods=["POST"])
def api_basket_compare():
    data = request.get_json() or {}
    items = data.get("items", [])
    if not items:
        # Default typical gym stack if empty
        items = [
            {"category": "Суроватъчен изолат"},
            {"category": "Креатин"}
        ]
    comparison = compare_basket(items)
    return jsonify({
        "status": "success",
        "result": comparison
    })

@app.route("/api/advisor", methods=["POST"])
def api_advisor():
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"status": "error", "message": "Query cannot be empty"}), 400

    advice_result = advise(query)
    return jsonify({
        "status": "success",
        "result": advice_result
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5055))
    print(f"🚀 [FitRadar BG] Server running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
