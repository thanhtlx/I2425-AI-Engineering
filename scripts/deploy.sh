pip install -r reqs.txt 
export MODEL_PATH="output"
export DAGSHUB_TOKEN='9b376c0de034c9caeca7346bf22a198ada8eeb58'
uvicorn model_deploying.deploy:app --reload