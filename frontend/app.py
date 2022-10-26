import streamlit as st
import json
import requests as re

st.title("Credit Card Fraud Detection Web App")

# st.image("image.png")

st.write("""
## About
Credit card fraud is a form of identity theft that involves an unauthorized taking of another's credit card information for the purpose of charging purchases to the account or removing funds from it.

**This Streamlit App utilizes a Machine Learning model served as an API in order to detect fraudulent credit card transactions based on the following criteria: hours, type of transaction, amount, balance before and after transaction etc.**

The API was built with FastAPI and can be found [here.](https://credit-fraud-ml-api.herokuapp.com/)

The notebook, model and documentation(Dockerfiles, FastAPI script, Streamlit App script) are available on [GitHub.](https://github.com/Nneji123/Credit-Card-Fraud-Detection)

""")


st.sidebar.header("Input Features of the Transaction")

sender_name = st.sidebar.text_input("Input Sender ID")
receiver_name = st.sidebar.text_input("Input Receiver ID")
step = st.sidebar.slider("Number of hours it took the Transaction to complete: ")
types = st.sidebar.subheader(f"""
Entery Type of Transfer Made:
0 for 'Cash In' Transaction
1 for 'Cash Out' Transaction
2 for 'Debit' Transaction
3 for 'Payment' Transaction
4 for 'Transfer' Transaction

""")

types = st.sidebar.selectbox("", (0,1,2,3,4))
x = ""
if types == 0:
    x = "Cash In"
elif types == 1:
    x = "Cash Out"
elif types == 2:
    x = "Debit"
elif types == 3:
    x = "Payment"
elif types == 4:
    x = "Transfer"

amount = st.sidebar.number_input("Amount in $", min_value=0, max_value=110000, key=1)
oldbalanceorg = st.sidebar.number_input("Original Balance Before Transaction was made", min_value=0, max_value=110000, key=2)
newbalanceorg = st.sidebar.number_input("Original Balance Before Transaction was made", min_value=0, max_value=110000, key=3)
oldbalancedest= st.sidebar.number_input("Old Balance", min_value=0, max_value=110000, key=4)
newbalancedest= st.sidebar.number_input("New Balance", min_value=0, max_value=110000, key=5)
isflaggedfraud = 1 if amount >= 200000 else 0


if st.button("Detection Result"):
    values = {
        "step" : step,
        "types" : types,
        "amount" : amount,
        "oldbalanceorig" : oldbalanceorg,
        "newbalanceorig" : newbalanceorg,
        "oldbalancedest" : oldbalancedest,
        "newbalancedest" : newbalancedest,
        "isflaggedfraud" : isflaggedfraud
    }

    st.write(f"""
    ### These are the transaction details:
    Sender ID: {sender_name}
    Receiver ID: {receiver_name}
    1. Number of hours it took to complete: {step}
    2. Type of Transaction: {x}
    3. Amount Sent: {amount}
    4. Previous Balance Before Transaction: {oldbalanceorg}
    5. New Balance After Transaction: {newbalanceorg}
    6. Old Balance Destination Recepient Balance: {oldbalancedest}
    7. New Balance Destination Recepient Balance: {newbalancedest}
    8. System Flag Fraud Status: {isflaggedfraud}
    """)

    res = re.post(f"https://backend.docker:8000/predict", json=values)
    json_str = json.dumps(res.json());
    resp = json.loads(json_str)

    if sender_name == '' or receiver_name == '':
        st.write("Error! Please input Transaction ID or Names of Sender and Receiver!")
    else:
        st.write(f"""### The '{x}' transaction that took place between {sender_name} and {receiver_name} is {resp[0]}""")
