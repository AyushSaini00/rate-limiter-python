import time
from typing import Dict, List

# in this algo, instead of a fixed window, the window shifts continously with time
# there is max threshold (eg: 3 req per 10 sec window)
# for each request, we track the timestamp if the request is accepted
# if the request exceeds the max threshold it is discarded

class SlidingWindowLog:
    def __init__(self, window_size: int, max_requests_per_window: int):
        self.window_size = window_size
        self.max_requests_per_window = max_requests_per_window
        self.logs: Dict[str, List[float]] = {} # { client_id: [ timestamp_of_requests ] }
        
    def allow_request(self, client_id: str):
        now = time.time()

        if not client_id in self.logs:
            self.logs[client_id] = []

        new_logs = []
        for timestamp in self.logs[client_id]:
            if timestamp > now - self.window_size:
                new_logs.append(timestamp)

        self.logs[client_id] = new_logs

        if len(self.logs[client_id]) >= self.max_requests_per_window:
            return False

        self.logs[client_id].append(now)
        return True