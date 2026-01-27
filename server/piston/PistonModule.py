import requests
import time
from threading import Lock

class PistonAPI:
    def __init__(self):
        self.base_url = "https://emkc.org/api/v2/piston"
        self.last_request_time = 0
        self.lock = Lock()
        self.min_interval = 0.2  # 5 req/sec = 0.2 sec between requests
    
    def _rate_limit(self):
        """Ensure we don't exceed 5 requests per second"""
        with self.lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.min_interval:
                time.sleep(self.min_interval - time_since_last)
            
            self.last_request_time = time.time()
    
    def execute(self, language, code, stdin="", timeout=10):
        self._rate_limit()
        
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json={
                    "language": language,
                    "version": "*",
                    "files": [{"content": code}],
                    "stdin": stdin
                },
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_languages(self):
        """Get list of supported languages"""
        response = requests.get(f"{self.base_url}/runtimes")
        return response.json()