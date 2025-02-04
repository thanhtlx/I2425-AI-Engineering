pip install -r reqs.txt 
export MODEL_PATH="output"
# hidden
uvicorn model_deploying.deploy:app --reload