def analyze_behavior(features):

    score = 0

    blink_rate = features["blink_rate"]
    gaze_rate = features["gaze_rate"]

    # ---------------- BLINK ----------------
    if blink_rate > 0.5:
        score += 30
    elif blink_rate > 0.3:
        score += 20
    elif blink_rate > 0.15:
        score += 10

    # ---------------- GAZE (BALANCED) ----------------
    if gaze_rate > 8:
        score += 30
    elif gaze_rate > 5:
        score += 20
    elif gaze_rate > 2:
        score += 10

    return min(score, 100)