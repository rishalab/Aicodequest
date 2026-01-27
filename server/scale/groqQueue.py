import queue
import threading
import time

class GroqQueue:
    def __init__(self, ai_module):
        self.ai = ai_module
        self.q = queue.Queue()
        self.worker = threading.Thread(target=self._worker, daemon=True)
        self.worker.start()

    def submit(self, fn, *args, **kwargs):
        result_q = queue.Queue()
        self.q.put((fn, args, kwargs, result_q))
        return result_q.get()  # blocks until done

    def _worker(self):
        while True:
            fn, args, kwargs, result_q = self.q.get()
            try:
                result = fn(*args, **kwargs)
                result_q.put(result)
            except Exception as e:
                result_q.put(e)
            time.sleep(2)  # 30 RPM safety
