class GazeDetector:

    def __init__(self):
        self.prev_direction = "CENTER"
        self.gaze_changes = 0

    def detect(self, ratio):

        if ratio < 2.75:
            direction = "LEFT"
        elif ratio > 2.95:
            direction = "RIGHT"
        else:
            direction = "CENTER"

        gaze_changed = False

    # 🔥 ONLY COUNT IF STABLE CHANGE
        if direction != self.prev_direction:

        # ignore CENTER flicker
            if not (self.prev_direction == "CENTER" and direction == "CENTER"):
                self.gaze_changes += 1
                gaze_changed = True

        self.prev_direction = direction

        return direction, self.gaze_changes, gaze_changed