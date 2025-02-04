FROM python:3.10-slim

# Set working directory
WORKDIR /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering
COPY . /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering

# Install dependencies
RUN apt-get update -y && apt-get install -y curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r reqs.txt

# Create necessary directories
RUN mkdir -p /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/output

# Download & extract AutogluonModels
RUN curl -L -o /tmp/AutogluonModels.zip "https://storage.googleapis.com/fraud-detection-model-i2425/final_model/deploy/AutogluonModels.zip" \
    && unzip /tmp/AutogluonModels.zip -d /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/AutogluonModels \
    && rm /tmp/AutogluonModels.zip \
    && ls -l

# Download model.pkl
RUN curl -L -o /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/output/model.pkl "https://storage.googleapis.com/fraud-detection-model-i2425/final_model/deploy/model.pkl"

# Set environment variables
ENV MODEL_PATH=/home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/output/model.pkl

# Expose FastAPI's default port
EXPOSE 8080

# Run FastAPI app
CMD ["uvicorn", "model_deploying.deploy:app", "--host", "0.0.0.0", "--port", "8080"]