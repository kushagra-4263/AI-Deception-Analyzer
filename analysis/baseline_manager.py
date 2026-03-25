import time


class BaselineManager:
    def __init__(self, duration=10):
        self.duration = duration
        self.start_time = None

        self.blink_count = 0
        self.gaze_changes = 0
        self.frame_count = 0

        self.last_gaze = None

        self.baseline = None
        self.is_recording = False
        self.is_complete = False

    def start(self):
        self.start_time = time.time()
        self.is_recording = True
        self.is_complete = False

        self.blink_count = 0
        self.gaze_changes = 0
        self.frame_count = 0
        self.last_gaze = None

    def update(self, blink_detected, gaze_direction):
        if not self.is_recording:
            return

        self.frame_count += 1

        if blink_detected:
            self.blink_count += 1

        if self.last_gaze is not None and gaze_direction != self.last_gaze:
            self.gaze_changes += 1

        self.last_gaze = gaze_direction

        if time.time() - self.start_time >= self.duration:
            self._compute_baseline()

    def _compute_baseline(self):
        total_time = time.time() - self.start_time

        blink_rate = self.blink_count / total_time
        gaze_change_rate = self.gaze_changes / total_time

        self.baseline = {
            "blink_rate": blink_rate,
            "gaze_change_rate": gaze_change_rate
        }

        self.is_recording = False
        self.is_complete = True

    def get_baseline(self):
        return self.baseline