import threading
import time
from datetime import datetime

'''
Network analyser if one wants to use traffic data for something
'''


class NetworkAnalyser:
    _instance_lock = threading.Lock()
    _instance = None
    debug = False

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__init__()
            return cls._instance

    def __init__(self):
        # Initialize variables
        self.amt_request_s = 0
        self.amt_request_m = 0
        self.amt_request_total = 0

        self.amt_response_s = 0
        self.amt_response_m = 0
        self.amt_response_total = 0

        self.last_update_time = datetime.now()
        # Start a background thread to update requests per second and requests per minute
        self.start_background_thread()

    def start_background_thread(self):
        def update_metrics():
            while True:
                time.sleep(1)
                self.update_requests_per_second()
                self.update_responses_per_second()
                self.update_requests_per_minute()
                self.update_responses_per_minute()
                self.print_metrics()

        thread = threading.Thread(target=update_metrics, daemon=True)
        thread.start()

    def update_requests_per_second(self):
        self.amt_request_s = 0

    def update_responses_per_second(self):
        self.amt_response_s = 0

    def update_requests_per_minute(self):
        now = datetime.now()
        elapsed_time = now - self.last_update_time
        if elapsed_time.total_seconds() >= 60:
            self.amt_request_m = 0

    def update_responses_per_minute(self):
        now = datetime.now()
        elapsed_time = now - self.last_update_time
        if elapsed_time.total_seconds() >= 60:
            self.amt_response_m = 0
            self.last_update_time = now

    def record_request(self):
        self.amt_request_s += 1
        self.amt_request_m += 1
        self.amt_request_total += 1

    def record_response(self):
        self.amt_response_s += 1
        self.amt_response_m += 1
        self.amt_response_total += 1

    def print_metrics(self):
        if not self.debug:
            return
        print("\nMetrics:")
        print(f"Current Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"Last Updated Time: {self.last_update_time}")
        print(f"Requests in the Last Second: {self.amt_request_s}")
        print(f"Responses in the Last Second: {self.amt_response_s}")
        print(f"Requests in the Last Minute: {self.amt_request_m}")
        print(f"Responses in the Last Minute: {self.amt_response_m}")
        print(f"Total Requests: {self.amt_request_total}")
        print(f"Total Responses: {self.amt_response_total}")
