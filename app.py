from flask import Flask, request, jsonify
from flask_cors import CORS
from src.summarizer import summarize

app = Flask(__name__)
CORS(app)

@app.route("/summarize", methods=["POST"])
def summarize_text():
    data = request.get_json()
    text = data.get("text", "")
    length = data.get("length", "medium")

    result = summarize(text, length)
    return jsonify({"summary": result})


if __name__ == "__main__":
    app.run(debug=True)
