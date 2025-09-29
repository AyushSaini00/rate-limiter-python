from fastapi import FastAPI

app = FastAPI()

@app.get("/unlimited")
def read_unlimited():
    return "Unlimited. LFG!!!"

@app.get("/limited")
def read_limited():
    return "Limited, handle with care :("