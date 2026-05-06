from pyexpat import features
from urllib.parse import urlparse

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from feature_extraction import extract_features

app = Flask(__name__)
CORS(app)

# Load trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return "PhishDetect API is running"

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