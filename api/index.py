from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS
from dotenv import load_dotenv
import base64
import os

load_dotenv()  # 👈 loads .env

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return "Groq Vision API is running"

@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "Image not provided"}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_data_url = f"data:{image_file.content_type};base64,{image_base64}"

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "Analyze the image and give the response in the specified json format:\n"
                    "{\n"
                    "isTextReadable: true or false,\n"
                    "extractedText: leave empty if isTextReadable is false,\n"
                    "shortDescription: Short Description about the image,\n"
                    "longDescription: Long Description\n"
                    "}"
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": ""},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url
                        }
                    }
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=2000,
    )
    print("there")
    print(jsonify({
        "response": completion.choices[0].message.content
    }))
    print(completion.choices[0].message.content)
    print("here")
    return jsonify({
        "response": completion.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
