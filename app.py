from fastapi import FastAPI, File, Query, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, PlainTextResponse, HTMLResponse
import uvicorn
import joblib
import numpy as np
from pydantic import BaseModel

app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="An API that utilises a Machine Learning model that detects if a credit card transaction is fraudulent or not based on the following features: hours, amount, transaction type etc.",
    version="1.0.0",
    debug=True
)

model = joblib.load('backend/credit_fraud.pkl');

@app.get("/", response_class=HTMLResponse)
async def running():
    return """
    <html>
        <head>
            <link rel="icon" type="image/x-icon" href="favicon.png">
            <title> API </title>
        </head>
        <body>
            <h2>Credit Card Fraud Detection API</h2>
            <p>Note: add "/docs" or "/redoc" to the URL to access the documentation</p>
            <p> OR </p>
            <div><a href="/docs"> Docs </a></div>
            <div><a href="/redoc"> Alternative Docs</a></div>
        </body>
    </html>
    """

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
    isflaggedfraud: float;

@app.post('/predict')
def predict(data: CreditData):
    features = np.array( [[data.step,
                           data.types,
                           data.amount,
                           data.oldbalanceorig,
                           data.newbalanceorig,
                           data.oldbalancedest,
                           data.newbalancedest,
                           data.isflaggedfraud]] );
    model = joblib.load('credit_fraud.pkl');
    predictions = model.predict(features);

    if (predictions == 1):
        return {"fraudulent"}
    elif (predictions == 0):
        return {"not fraudulent"}
