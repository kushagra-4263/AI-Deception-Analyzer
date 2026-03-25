from utils.math_utils import distance


class BlinkDetector:
    def __init__(self, threshold=0.20, closed_frames=3):
        self.blink_threshold = threshold
        self.closed_frames = closed_frames

        self.frame_counter = 0
        self.blink_count = 0

    def detect(self, left_eye_points, right_eye_points):

        vertical1_l = distance(left_eye_points[1], left_eye_points[5])
        vertical2_l = distance(left_eye_points[2], left_eye_points[4])
        horizontal_l = distance(left_eye_points[0], left_eye_points[3])

        left_EAR = (vertical1_l + vertical2_l) / (2.0 * horizontal_l)

        vertical1_r = distance(right_eye_points[1], right_eye_points[5])
        vertical2_r = distance(right_eye_points[2], right_eye_points[4])
        horizontal_r = distance(right_eye_points[0], right_eye_points[3])

        right_EAR = (vertical1_r + vertical2_r) / (2.0 * horizontal_r)

        EAR = (left_EAR + right_EAR) / 2

        blink_detected = False

        if EAR < self.blink_threshold:
            self.frame_counter += 1
        else:
            if self.frame_counter >= self.closed_frames:
                self.blink_count += 1
                blink_detected = True   # 👈 important change
            self.frame_counter = 0

        return blink_detected, EAR, self.blink_count