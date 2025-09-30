from fastapi import FastAPI, Request, Depends, HTTPException
from token_bucket import TokenBucket
from fixed_window_counter import FixedWindowCounter
from sliding_window_log import SlidingWindowLog
from typing import Dict, List
import time
from enum import Enum

app = FastAPI()

class AlgoTypes(Enum):
    TOKEN_BUCKET = "token_bucket"
    FIXED_WINDOW_COUNTER = "fixed_window_counter"
    SLIDING_WINDOW_LOG = "sliding_window_log"

token_buckets: Dict[str, 'TokenBucket'] = {}
fixed_window_counters: Dict[str, Dict[int, int]] = {} # { client_id: { window_start: count } }
sliding_window_logs: Dict[str, List[float]] = {} # { client_id: [ timestamp_of_requests ] }

# dependency injection https://fastapi.tiangolo.com/tutorial/dependencies/
def rate_limiter(algo_type: AlgoTypes):
    def _rate_limiter(request: Request):
        client_id = request.client.host

        match algo_type:
            case AlgoTypes.TOKEN_BUCKET:
                if client_id not in token_buckets:
                    token_buckets[client_id] = TokenBucket(10, 1)

                bucket = token_buckets[client_id]
                if not bucket.allow_request():
                    raise HTTPException(status_code=429, detail="Too many requests")
                
            case AlgoTypes.FIXED_WINDOW_COUNTER:
                windowCounter = FixedWindowCounter(window_size=60, max_requests_per_window=60, fixed_window_counters=fixed_window_counters)
                if not windowCounter.allow_request(client_id):
                    raise HTTPException(status_code=429, detail="Too many requests") 
            
            case AlgoTypes.SLIDING_WINDOW_LOG:
                slidingWindowLog = SlidingWindowLog(window_size=30, max_requests_per_window=60, sliding_window_logs=sliding_window_logs)

                if not slidingWindowLog.allow_request(client_id):
                    raise HTTPException(status_code=429, detail="Too many requests")

            case _:
                raise HTTPException(status_code=500, detail="unknown rate limiting algo")

    return _rate_limiter       

@app.get("/unlimited")
def read_unlimited():
    return "Unlimited. LFG!!!"

@app.get("/limited", dependencies=[Depends(rate_limiter(AlgoTypes.SLIDING_WINDOW_LOG))])
def read_limited(request: Request):
    return "Limited, handle with care :(" 