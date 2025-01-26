from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_deploying.utils.utils import process_user_input
import numpy as np
import joblib
import os
from fastapi import Body


class Transaction(BaseModel):
    merchant: int
    category: str
    amt: float
    gender: str
    lat: float
    long: float
    city_pop: int
    job: str
    unix_time: int
    merch_lat: float
    merch_long: float
    trans_date_trans_time: str

    def to_dict(self):
        return {
            "trans_date_trans_time":self.trans_date_trans_time,
            "merchant": self.merchant,
            "category": self.category,
            "amt": self.amt,
            "gender": self.gender,
            "lat": self.lat,
            "long": self.long,
            "city_pop": self.city_pop,
            "job": self.job,
            "unix_time": self.unix_time,
            "merch_lat": self.merch_lat,
            "merch_long": self.merch_long,
        }


# Define the FastAPI app
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})


model_path = os.getenv("MODEL_PATH", "model.pkl")
# Load the pre-trained SVC model (ensure to replace 'svc_model.pkl' with your actual model file path)
try:
    model = joblib.load(model_path)
except Exception as e:
    raise RuntimeError(f"Failed to load model from {model_path}: {e}")


@app.get("/health")
def health():
    return {"status": "ok"}


# Endpoint for making predictions
@app.post("/predict")
def predict(data: Transaction):
    print(data.to_dict())
    features = process_user_input(data.to_dict())
    try:
        # Perform prediction
        print('features',features)
        prediction = model.predict(features)
        probability = (
            model.predict_proba(features)
            if hasattr(model, "predict_proba")
            else 1
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")

    # Return prediction result
    response = {"prediction": prediction[0].item(), "probability": probability}
    print(response)
    return response
