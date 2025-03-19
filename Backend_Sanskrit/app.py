from flask import Flask, request, jsonify, Response
import requests
from fill_in_the_blank import generate_fill_in_the_blank
from image_generation import generate_image
from writing_analysis import analyze_writing
from translation import generate_translation_exercise
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

@app.route('/')
def home():
    return "Sanskrit Learning API is Running!"

@app.route('/fill-in-the-blank', methods=['GET'])
def fill_in_the_blank():
    result = generate_fill_in_the_blank()
    return jsonify(result)

@app.route('/generate-image', methods=['GET'])
def image_generation():
    data = request.get_json()
    prompt = data.get("prompt", "")
    print(prompt)
    image_url, options, correct_answer = generate_image(client, prompt)
    return jsonify({"image_url": image_url, "options": options, "correct_answer": correct_answer})

@app.route('/writing-analysis', methods=['GET'])
def writing_analysis():
    data = request.get_json()
    text = data.get("text", "")
    print(text)
    feedback = analyze_writing(text)
    print(feedback)
    return jsonify({"feedback": feedback})

@app.route('/translate', methods=['GET'])
def translate():
    result = generate_translation_exercise(client)
    return jsonify(result)

@app.route('/proxy-image')
def proxy_image():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "Missing image URL"}), 400
    try:
        response = requests.get(image_url, stream=True)
        content_type = response.headers.get('Content-Type', 'image/png')
        return Response(response.content, content_type=content_type)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch image: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
