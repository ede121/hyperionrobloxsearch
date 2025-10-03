from flask import Flask, request, jsonify
import requests
import os

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
        # Query Roblox catalog with proper headers
        url = f"https://catalog.roblox.com/v1/search/items?limit=20&keyword={keyword}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("data", []):
            if item.get("id") and item.get("itemType") == "Asset":
                results.append({
                    "id": item["id"],
                    "name": item.get("name", f"Asset {item['id']}"),
                    "imageUrl": f"https://www.roblox.com/asset-thumbnail/image?assetId={item['id']}&width=150&height=150&format=png"
                })

        return jsonify({"results": results})

    except requests.exceptions.RequestException as e:
        print("HTTP request failed:", e)
        return jsonify({"error": "Failed to fetch Roblox catalog"}), 500
    except Exception as e:
        print("Unexpected error:", e)
        return jsonify({"error": "Failed to fetch Roblox catalog"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
