FROM python:3.10-slim

# Set working directory
WORKDIR /app
COPY . /app

# Install dependencies
RUN apt-get update -y && apt-get install -y curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r reqs.txt

# Create necessary directories
RUN mkdir -p /app/output

# Download & extract AutogluonModels
RUN curl -L -o /tmp/AutogluonModels.zip "https://storage.googleapis.com/fraud-detection-model-i2425/final_model/deploy/AutogluonModels.zip" \
    && unzip /tmp/AutogluonModels.zip -d /app/AutogluonModels \
    && rm /tmp/AutogluonModels.zip \
    && ls -l

# Download model.pkl
RUN curl -L -o /app/output/model.pkl "https://storage.googleapis.com/fraud-detection-model-i2425/final_model/deploy/model.pkl"

# Set environment variables
ENV MODEL_PATH=/app/output/model.pkl

# Expose FastAPI's default port
EXPOSE 8080

# Run FastAPI app
CMD ["uvicorn", "model_deploying.deploy:app", "--host", "0.0.0.0", "--port", "8080"]