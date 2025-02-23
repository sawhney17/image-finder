from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
# handling CORS issues for tihs 
CORS(app) 

def get_first_image_url(query):
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    if len(img_tags) > 2:
        return img_tags[2]["src"]
    return None

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    image_url = get_first_image_url(query)
    return jsonify({"query": query, "image_url": image_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)