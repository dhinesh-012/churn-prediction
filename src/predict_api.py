# src/predict_api.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("models/churn_pipeline.joblib")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # data should be a dict or list of dicts
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame(data)
    # model expects same columns as training (preprocessing will handle unknown categories)
    proba = model.predict_proba(df)[:,1]
    pred = model.predict(df)
    return jsonify({"pred": pred.tolist(), "probability": proba.tolist()})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
