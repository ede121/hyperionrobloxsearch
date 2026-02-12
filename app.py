from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)



SEARCH_URL = "https://apis.roblox.com/toolbox-service/v1/marketplace/13"
DETAILS_URL = "https://apis.roblox.com/toolbox-service/v1/items/details"

@app.route("/")
def home():
    return "Roblox Image Search Backend is running!"

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Missing keyword"}), 400

    try:
        # 1️⃣ Search for asset IDs
        search_params = {
            "limit": 10,  # change as needed
            "pageNumber": 0,
            "keyword": keyword,
            "includeOnlyVerifiedCreators": "false"
        }
        search_resp = requests.get(SEARCH_URL, params=search_params)
        search_resp.raise_for_status()
        search_data = search_resp.json()

        asset_ids = {}
        for item in search_data.get("data", []):
            if item.get("id"):
                asset_ids[item["id"]] = None  # store IDs as keys

        if not asset_ids:
            return jsonify({"results": []})  # no assets found

        # 2️⃣ Get details for all asset IDs
        details_params = {
            "assetIds": ",".join(str(aid) for aid in asset_ids.keys())
        }
        details_resp = requests.get(DETAILS_URL, params=details_params)
        details_resp.raise_for_status()
        details_data = details_resp.json()

        results = []
        for item in details_data.get("data", []):
            asset = item.get("asset", {})
            creator = item.get("creator", {})
            texture_id = asset.get("textureId") or 0  # fallback if missing
            results.append({
                "id": asset.get("id"),
                "name": asset.get("name"),
                "imageUrl": f"https://www.roblox.com/asset-thumbnail/image?assetId={texture_id}&width=150&height=150&format=png",
                "creator": creator.get("name", "Unknown")
            })

        return jsonify({"results": results})

    except Exception as e:
        print("Error fetching Roblox assets:", e)
        return jsonify({"error": "Failed to fetch Roblox assets"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
