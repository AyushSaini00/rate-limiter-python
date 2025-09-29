from fastapi import FastAPI, Request, Depends, HTTPException
from token_bucket import TokenBucket
from typing import Dict

app = FastAPI()

token_buckets: Dict[str, 'TokenBucket'] = {}

def rate_limiter(request: Request):
    client_id = request.client.host

    if client_id not in token_buckets:
        token_buckets[client_id] = TokenBucket(10, 1)

    bucket = token_buckets[client_id]

    if not bucket.allow_request():
        raise HTTPException(status_code=429, detail="Too many requests")

@app.get("/unlimited")
def read_unlimited():
    return "Unlimited. LFG!!!"

@app.get("/limited", dependencies=[Depends(rate_limiter)])
def read_limited(request: Request):
    return "Limited, handle with care :(" 