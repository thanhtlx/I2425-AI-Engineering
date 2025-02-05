from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from model_deploying.utils.utils import process_user_input
import os
import mlflow
from time import time
from autogluon.tabular import TabularPredictor
import dagshub

dagshub_token = os.getenv("DAGSHUB_TOKEN")
dagshub.auth.add_app_token(dagshub_token)  # Authenticate using the token
dagshub.init(
    repo_owner="vrykolakas166",
    repo_name="fraud-detection-model-versioning",
    mlflow=True,
)
mlflow_tracking_uri = (
    "https://dagshub.com/vrykolakas166/fraud-detection-model-versioning.mlflow"
)


class Transaction(BaseModel):
    merchant: str
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
            "trans_date_trans_time": self.trans_date_trans_time,
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


# Global variable for model
model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model_path = os.getenv("MODEL_PATH", "svc_model.pkl")  # Use correct path
    try:
        model = TabularPredictor.load(model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load model: {e}")

    # Set MLflow tracking URI and experiment
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment("FastAPI Model Monitoring")
    yield  # Keep the app running
    print("🛑 Shutting down...")


# Define the FastAPI app
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True}, lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


# Endpoint for making predictions
@app.post("/predict")
def predict(data: Transaction):
    features = process_user_input(data.to_dict())
    # Set the MLflow registry URI
    with mlflow.start_run():
        start_time = time()
        try:
            # Perform prediction
            prediction = model.predict(features)
            probability = (
                model.predict_proba(features)
                if hasattr(model, "predict_proba")
                else None
            )
        except Exception as e:
            mlflow.log_metric("failed_requests", 1)
            raise HTTPException(status_code=400, detail=f"Prediction error: {e}")

        # Calculate latency
        latency = time() - start_time

        # Log metrics to MLflow
        mlflow.log_metric("latency", latency)
        mlflow.log_metric("amt", data.amt)
        mlflow.log_metric("city_pop", data.city_pop)
        mlflow.log_metric("successful_requests", 1)

        # Optional: Log predictions
        prediction = float(prediction.item())
        probability = float(dict(probability)[1].item())
        mlflow.log_param("prediction", prediction)
        if probability is not None:
            mlflow.log_metric("probability", probability)

        # Return prediction result
        response = {
            "prediction": prediction,
            "probability": probability,
        }
        return response
