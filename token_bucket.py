import time
from typing import Dict

# TokenBucket will create a bucket with max_capacity per user (eg: 10 tokens)
# tokens are refilled at a fixed rate (eg: 1 token per second)
# each request will consume 1 token
# if bucket is empty -> request will be rejected

class TokenBucket:
    def __init__(self, max_capacity: int, refill_rate: int):
        self.max_capacity = max_capacity
        self.refill_rate = refill_rate
        self.buckets: Dict[str, Dict[str, float]] = {}

    def allow_request(self, client_id: str):
        now = time.time()
        
        if client_id not in self.buckets:
            self.buckets[client_id] = {
                'tokens': self.max_capacity,
                'last_refill': now
            }

        bucket = self.buckets[client_id]

        elapsed = now - bucket['last_refill']
        new_tokens = self.refill_rate * elapsed # this number of tokens should have been added

        #but bucket's max size is max_capacity, so updating the no. of tokens
        bucket['tokens'] = min(self.max_capacity, bucket['tokens'] + new_tokens)
        # updating the last refill time
        bucket['last_refill'] = now

        if bucket['tokens'] >= 1:
            bucket['tokens'] = bucket['tokens'] - 1
            return True
        else:
            return False
