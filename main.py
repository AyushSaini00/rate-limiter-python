from fastapi import FastAPI, Request, Depends, HTTPException
from token_bucket import TokenBucket
from fixed_window_counter import FixedWindowCounter
from sliding_window_log import SlidingWindowLog
from sliding_window_counter import SlidingWindowCounter
from enum import Enum

app = FastAPI()

class AlgoTypes(Enum):
    TOKEN_BUCKET = "token_bucket"
    FIXED_WINDOW_COUNTER = "fixed_window_counter"
    SLIDING_WINDOW_LOG = "sliding_window_log"
    SLIDING_WINDOW_COUNTER = "sliding_window_counter"    

# creating instances of algorithms
rate_limiters = {
   AlgoTypes.TOKEN_BUCKET: TokenBucket(max_capacity=10, refill_rate=1),
   AlgoTypes.FIXED_WINDOW_COUNTER: FixedWindowCounter(window_size=60, max_requests_per_window=60),
   AlgoTypes.SLIDING_WINDOW_LOG: SlidingWindowLog(window_size=30, max_requests_per_window=60),
   AlgoTypes.SLIDING_WINDOW_COUNTER: SlidingWindowCounter(window_size=60, max_requests_per_window=60)
}

# dependency injection https://fastapi.tiangolo.com/tutorial/dependencies/
def rate_limiter(algo_type: AlgoTypes):
    def _rate_limiter(request: Request):
        client_id = request.client.host
        limitter = rate_limiters.get(algo_type)
        
        if not limitter:
            raise HTTPException(status_code=500, detail="unknown rate limiting algo")
        
        if not limitter.allow_request(client_id):
            raise HTTPException(status_code=429, detail="Too many requests")

    return _rate_limiter       

@app.get("/unlimited")
def read_unlimited():
    return "Unlimited. LFG!!!"

@app.get("/limited", dependencies=[Depends(rate_limiter(AlgoTypes.SLIDING_WINDOW_COUNTER))])
def read_limited(request: Request):
    return "Limited, handle with care :(" 