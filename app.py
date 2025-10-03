from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Roblox Image Search Backend is running!"

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Missing keyword"}), 400

    try:
        # Query Roblox catalog
        url = f"https://catalog.roblox.com/v1/search/items?limit=20&keyword={keyword}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Filter assets and build safe results
        results = []
        for item in data.get("data", []):
            if item.get("id") and item.get("itemType") == "Asset":
                results.append({
                    "id": item["id"],
                    "name": item.get("name", f"Asset {item['id']}"),
                    "imageUrl": f"https://www.roblox.com/asset-thumbnail/image?assetId={item['id']}&width=150&height=150&format=png"
                })

        return jsonify({"results": results})

    except Exception as e:
        print("Error fetching catalog:", e)
        return jsonify({"error": "Failed to fetch Roblox catalog"}), 500


if __name__ == "__main__":
    # Render automatically sets PORT environment variable
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
