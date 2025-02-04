FROM python:3.10-slim

# Set working directory
WORKDIR /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering

# Copy only required files to reduce build size
COPY model_deploying /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/model_deploying
COPY reqs.txt /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/reqs.txt    

# Install dependencies
RUN apt-get update -y && apt-get install -y curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r reqs.txt

# Create necessary directories
RUN mkdir -p /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/output

# Download & extract AutogluonModels
RUN curl -L -o /tmp/AutogluonModels.zip "https://storage.googleapis.com/fraud-detection-model-i2425/final_model/deploy/AutogluonModels.zip" \
    && rm -rf /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/output/* \
    && unzip /tmp/AutogluonModels.zip -d /home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/output \
    && rm /tmp/AutogluonModels.zip

# Set environment variables
ENV PORT=8080
ENV MODEL_PATH=/home/runner/work/I2425-AI-Engineering/I2425-AI-Engineering/output

# Expose FastAPI's default port
EXPOSE 8080

# Run FastAPI app
CMD ["uvicorn", "model_deploying.deploy:app", "--host", "0.0.0.0", "--port", "8080"]