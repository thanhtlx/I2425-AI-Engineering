pip install -r reqs.txt 
export MODEL_PATH="output/model.pkl"
uvicorn model_deploying.deploy:app --reload