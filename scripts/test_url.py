import pandas as pd 
df = pd.read_csv("data/test.csv")
columns = [
            "trans_date_trans_time",
            "merchant",
            "category",
            "amt",
            "gender",
            "lat",
            "long",
            "city_pop",
            "job",
            "unix_time",
            "merch_lat",
            "merch_long",
    ]
url = "http://localhost:8000/predict"  
import requests

for _,row in df.sample(100).iterrows():
    body = dict()
    for cl in columns:
        body[cl] = row[cl]
    response = requests.post(url, json=body)
    print("#" * 5, "LOG", "#" * 5)
    if response.status_code == 200:
        print("Prediction Response:", response.json())
    else:
        print("Failed with status code:", response.status_code)
        print("Error:", response.text)
    print('_'*20)
