import time
from typing import Dict

# this is an approximation of sliding window log that avoids storing every single timestamp
# instead of looking at the current window, we also look at the previous window and how much it still overlaps with sliding window

class SlidingWindowCounter:
    def __init__(self, window_size: int, max_requests_per_window: int):
        self.window_size = window_size
        self.max_requests_per_window = max_requests_per_window
        self.counters: Dict[str, Dict[int, int]] = {} # { client_id: { curr_window: count } }
        
    def allow_request(self, client_id: str):
        now = time.time()

        curr_window = int(now // self.window_size)
        prev_window = curr_window - 1

        if client_id not in self.counters:
            self.counters[client_id] = {}

        # clean-up old windows
        updated_counters = {}
        windows_to_keep = {curr_window, prev_window}
        for window, count in self.counters[client_id].items():
            if window in windows_to_keep:
                updated_counters[window] = count
                
        self.counters[client_id] = updated_counters        

        curr_count = self.counters[client_id].get(curr_window, 0) # get(key, default) -> will return 0 if curr_window doesn't exist on the dict
        prev_count = self.counters[client_id].get(prev_window, 0)

        elapsed = now % self.window_size # how much time has passed since the start of current window
        overlap = 1 - (elapsed / self.window_size) #how much of the previous window still matters

        count = int(curr_count + prev_count * overlap) # so essentially the client has made count no. of requests in the sliding window

        if count >= self.max_requests_per_window:
            return False
        
        self.counters[client_id][curr_window] = curr_count + 1
        return True
