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
        self.last_refill_timestamp = time.time()
        self.tokens = max_capacity # current number of tokens, lets start with max_capacity

    def allow_request(self):
        now = time.time()
        elapsed = now - self.last_refill_timestamp
        new_tokens = self.refill_rate * elapsed # this number of tokens should have been added
        #but bucket's max size is max_capacity, so updating the no. of tokens
        self.tokens = min(self.max_capacity, self.tokens + new_tokens)
        # updating the last refill time
        self.last_refill_timestamp = now

        if self.tokens >= 1:
            self.tokens = self.tokens - 1
            return True
        else:
            return False
