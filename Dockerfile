FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Install dependencies
RUN apt update -y && apt-get install -y curl
RUN pip install --no-cache-dir -r reqs.txt

# Create the models directory
RUN mkdir -p /app/models

# Download the model.pkl from DagsHub
# TODO: model.pkl need whole AutogluonModels folder to be loaded
RUN curl -L -o /app/models/model.pkl "https://dagshub.com/vrykolakas166/fraud-detection-model-versioning/raw/main/final_model/02_01_2025_07_35_44/model.pkl"

# Set environment variables
ENV MODEL_PATH=/app/models/model.pkl

# Expose FastAPI's default port
EXPOSE 8080

# Run the FastAPI app (updated to point to model_deploying/deploy.py)
CMD ["uvicorn", "model_deploying.deploy:app", "--host", "0.0.0.0", "--port", "8080"]