from pyexpat import features
from urllib.parse import urlparse

from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
import os
import pickle
from feature_extraction import extract_features

app = Flask(
    __name__,
    static_folder="../frontend/dist",
    static_url_path=""
)

CORS(app)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    file_path = os.path.join(app.static_folder, path)

    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)

    return send_from_directory(app.static_folder, "index.html")


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data['url']

    # ✅ RULE-BASED CHECKS (ADD HERE)
    if not url.startswith("http"):
        return jsonify({"result": "Invalid URL", "confidence": 100})

    if "@" in url:
        return jsonify({"result": "Phishing",
                         "confidence": 100
                        })

    if any(word in url.lower() for word in ["login", "bank", "verify", "update"]):
        return jsonify({"result": "Phishing",
                        "confidence": 90
                        })
    
    parsed = urlparse(url)

    if not parsed.scheme or not parsed.netloc:
        return jsonify({
            "result": "Invalid URL",
            "confidence": 0
        })

    features = extract_features(url)

    prediction = model.predict([features])[0]
    proba = model.predict_proba([features])[0]
    confidence = proba[prediction]

    return jsonify({
        "result": "Phishing" if prediction == 1 else "Safe",
        "confidence": round(confidence * 100, 2)
    })
if __name__ == '__main__':
    app.run(debug=True)
