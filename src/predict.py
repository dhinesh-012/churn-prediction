# src/predict.py
import joblib
import pandas as pd

def load_model():
    """Load the saved churn pipeline."""
    return joblib.load("models/churn_pipeline.joblib")

def make_prediction(model, input_data: dict):
    """Make a churn prediction for a new customer."""
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    return prediction, probability

if __name__ == "__main__":
    # Example new customer (replace values to test with your own data)
    new_customer = {
        "gender": "Female",
        "seniorcitizen": 0,
        "partner": "Yes",
        "dependents": "No",
        "tenure": 12,
        "phoneservice": "Yes",
        "multiplelines": "No",
        "internetservice": "Fiber optic",
        "onlinesecurity": "No",
        "onlinebackup": "Yes",
        "deviceprotection": "No",
        "techsupport": "No",
        "streamingtv": "Yes",
        "streamingmovies": "Yes",
        "contract": "Month-to-month",
        "paperlessbilling": "Yes",
        "paymentmethod": "Electronic check",
        "monthlycharges": 70.35,
        "totalcharges": 845.50
    }

    model = load_model()
    pred, proba = make_prediction(model, new_customer)

    print("Churn Prediction:", "Yes" if pred == 1 else "No")
    print(f"Churn Probability: {proba:.2f}")
