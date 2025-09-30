from typing import Dict
import time

# in this approach, we divide the time into fixed length windows (eg: 1 minute)
# for each window, we count the number of requests made by the client
# if the count exceeds the limit (eg: 100 per window), the requests are rejected
# at next window, counter resets to 0

class FixedWindowCounter:
    def __init__(self, window_size: int, max_requests_per_window: int, fixed_window_counters: Dict[str, Dict[int, int]]):
        self.window_size = window_size # in seconds
        self.max_requests_per_window = max_requests_per_window
        self.counters = fixed_window_counters

    def allow_request(self, client_id: str):
        current_time = int(time.time())
        window_start = current_time // self.window_size

        if client_id not in self.counters:
            self.counters[client_id] = {}

        if window_start not in self.counters[client_id]:
            self.counters[client_id][window_start] = 0

        self.counters[client_id][window_start] += 1

        if self.counters[client_id][window_start] <= self.max_requests_per_window:
            return True
        else:
            return False       
