import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or not api_key.startswith("sk-"):
    raise ValueError("❌ OPENAI_API_KEY missing or invalid.")

client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    return jsonify({"message": "✅ Text2Image Studio backend is running."})

@app.route("/generate", methods=["POST"])
def generate_image():
    try:
        data = request.get_json(force=True)
        prompt = data.get("prompt", "").strip()
        if not prompt:
            return jsonify({"error": {"message": "No prompt provided."}}), 400

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = result.data[0].url
        return jsonify({"image_url": image_url})

    except Exception as e:
        # Capture and return any OpenAI or Python errors
        return jsonify({"error": {"message": str(e)}}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
