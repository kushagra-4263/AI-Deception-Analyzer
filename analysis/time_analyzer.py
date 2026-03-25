import time

class TimeAnalyzer:

    def __init__(self):
        self.start_time = time.time()
        self.blink_count = 0
        self.gaze_changes = 0

    def update(self, blink_detected, gaze_changed):

        if blink_detected:
            self.blink_count += 1

        if gaze_changed:
            self.gaze_changes += 1

    def get_features(self):

        elapsed = time.time() - self.start_time

    # 🔥 IMPORTANT FIX
        if elapsed < 3:
            return {"blink_rate": 0, "gaze_rate": 0}

        return {
            "blink_rate": self.blink_count / elapsed,
            "gaze_rate" : (self.gaze_changes / elapsed) * 10
    }

    def reset(self):
        self.start_time = time.time()
        self.blink_count = 0
        self.gaze_changes = 0