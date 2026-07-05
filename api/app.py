from fastapi import FastAPI
import pickle
import pandas as pd

app = FastAPI()

# load model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/predict")
def predict(day: int, hour: int, item: str):

    item = item.capitalize()

    # create base input
    data = {
        "hour": hour,
        "day": day,
        "is_weekend": 1 if day >= 5 else 0,
        "item_Biryani": 0,
        "item_Burger": 0,
        "item_Pizza": 0,
        "item_Dosa": 0,
        "item_Idli": 0,
        "item_FriedRice": 0,
        "item_Noodles": 0
    }

    if item == "Biryani":
        data["item_Biryani"] = 1
    elif item == "Burger":
        data["item_Burger"] = 1
    elif item == "Pizza":
        data["item_Pizza"] = 1
    elif item == "Dosa":
        data["item_Dosa"] = 1
    elif item == "Idli":
        data["item_Idli"] = 1
    elif item == "FriedRice":
        data["item_FriedRice"] = 1
    elif item == "Noodles":
        data["item_Noodles"] = 1

    df = pd.DataFrame([data])

    df = df[[
    "hour",
    "day",
    "is_weekend",
    "item_Biryani",
    "item_Burger",
    "item_Dosa",
    "item_FriedRice",
    "item_Idli",
    "item_Noodles",
    "item_Pizza"
    ]]

    prediction = model.predict(df)[0]

    return {"predicted_orders": int(prediction)}
    return {"predicted_orders": int(prediction)}