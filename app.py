from fastapi import FastAPI, File
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import joblib
import numpy as np
from pydantic import BaseModel
import os

app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="An API that utilises a Machine Learning model that detects if a credit card transaction is fraudulent or not based on the following features: hours, amount, transaction type etc.",
    version="1.0.0",
    debug=True
)

model = joblib.load('objects/credit_fraud.pkl');

@app.get("/", response_class=HTMLResponse)
async def running():
    home = open(os.path.join("frontend/index.html"), 'r');
    html = home.read();
    home.close()
    return html

favicon_path = 'favicon.png'
@app.get('/favicon.png', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

class CreditData(BaseModel):
    step: int;
    types: int;
    amount: float;
    oldbalanceorig: float;
    newbalanceorig: float;
    oldbalancedest: float;
    newbalancedest: float;
    isFlaggedFraud: int;

@app.post('/predict/')
def predict(data: CreditData):
    print(data)
    features = np.array( [[data.step,
                           data.types,
                           data.amount,
                           data.oldbalanceorig,
                           data.newbalanceorig,
                           data.oldbalancedest,
                           data.newbalancedest,
                           data.isFlaggedFraud
                           ]] );
    model = joblib.load('objects/credit_fraud.pkl');
    predictions = model.predict(features);

    if (predictions == 1):
        return {"fraudulent"}
    elif (predictions == 0):
        return {"not fraudulent"}
