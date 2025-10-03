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
        url = f"https://catalog.roblox.com/v1/search/items?limit=10&keyword={keyword}"
        response = requests.get(url)
        response.raise_for_status()

        try:
            data = response.json()
        except Exception as json_err:
            print("JSON decode error. Response text:", response.text)
            raise json_err

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

    except requests.exceptions.RequestException as e:
        print("HTTP request failed:", e)
        return jsonify({"error": "Failed to fetch Roblox catalog"}), 500
    except Exception as e:
        print("Unexpected error:", e)
        return jsonify({"error": "Failed to fetch Roblox catalog"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
