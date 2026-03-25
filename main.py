import cv2
import mediapipe as mp

from detection.blink_detector import BlinkDetector
from detection.gaze_detector import GazeDetector
from analysis.behavior_analyzer import analyze_behavior
from analysis.baseline_manager import BaselineManager
from analysis.question_manager import QuestionManager
from analysis.response_analyzer import ResponseAnalyzer
from analysis.data_logger import DataLogger
from analysis.time_analyzer import TimeAnalyzer


# -------------------- UI FUNCTION --------------------
def draw_ui(frame, phase, question=None, score=None, q_index=None, total_q=None):

    cv2.rectangle(frame, (20, 20), (700, 350), (30, 30, 30), -1)

    cv2.putText(frame, f"PHASE: {phase}", (40, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

    if q_index is not None:
        cv2.putText(frame, f"Question: {q_index}/{total_q}", (40, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    if question is not None:
        cv2.putText(frame, f"Q: {question}", (40, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    if score is not None:
        cv2.putText(frame, f"Deception: {score}%", (40, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)


# -------------------- INIT --------------------
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera not opened")
else:
    print("✅ Camera opened")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

baseline_manager = BaselineManager(duration=10)
baseline_manager.start()

question_manager = QuestionManager()
response_analyzer = ResponseAnalyzer()
data_logger = DataLogger()

blink_detector = BlinkDetector()
gaze_detector = GazeDetector()
time_analyzer = TimeAnalyzer()

last_question = None
results_summary = []
questions_started = False

LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]
LEFT_IRIS = [474,475,476,477]


# -------------------- LOOP --------------------
while True:

    ret, frame = camera.read()

    if not ret:
        print("⚠ Frame not received")
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    blink_detected = False
    gaze_direction = "CENTER"
    gaze_changed = False

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            h, w, _ = frame.shape

            left_eye_points = []
            right_eye_points = []
            iris_points = []

            # -------- EYE LANDMARKS --------
            for idx in LEFT_EYE:
                lm = face_landmarks.landmark[idx]
                left_eye_points.append((int(lm.x*w), int(lm.y*h)))

            for idx in RIGHT_EYE:
                lm = face_landmarks.landmark[idx]
                right_eye_points.append((int(lm.x*w), int(lm.y*h)))

            for idx in LEFT_IRIS:
                lm = face_landmarks.landmark[idx]
                iris_points.append((int(lm.x*w), int(lm.y*h)))

            # -------- BLINK --------
            if len(left_eye_points) == 6 and len(right_eye_points) == 6:
                blink_detected, _, _ = blink_detector.detect(
                    left_eye_points, right_eye_points
                )

            # -------- GAZE --------
            if len(iris_points) == 4:

                iris_x = int(sum([p[0] for p in iris_points]) / 4)

                left_corner = left_eye_points[0]
                right_corner = left_eye_points[3]

                eye_width = max(right_corner[0] - left_corner[0], 1)
                iris_position = iris_x - left_corner[0]

                ratio = iris_position / eye_width

                # DEBUG (remove later)
                print("Ratio:", round(ratio, 2))

                direction, _, gaze_changed = gaze_detector.detect(ratio)
                gaze_direction = direction

                print("Gaze:", gaze_direction)

    # -------- TIME ANALYZER UPDATE --------
    time_analyzer.update(blink_detected, gaze_changed)

    # -------- BASELINE --------
    baseline_manager.update(blink_detected, gaze_direction)

    # ---------------- FLOW ----------------
    if not baseline_manager.is_complete:

        draw_ui(frame, "BASELINE")

    else:

        if not questions_started:
            question_manager.start()
            questions_started = True

        question_manager.update()
        question = question_manager.get_current_question()

        if question is not None:

            # -------- QUESTION CHANGE --------
            if last_question is not None and question != last_question:

    # ONLY RESET AFTER SOME DATA
                features = time_analyzer.get_features()

                if features["gaze_rate"] > 0 or features["blink_rate"] > 0:

                    final_score = response_analyzer.get_final_score()
                    data_logger.log(last_question, final_score)
                    results_summary.append((last_question, final_score))

                    response_analyzer.reset()
                    time_analyzer.reset()

            last_question = question

            # -------- FEATURE-BASED SCORING --------
            features = time_analyzer.get_features()
            print("FEATURES:", features)
            score = analyze_behavior(features)

            response_analyzer.add_score(score)
            final_score = response_analyzer.get_final_score()

            draw_ui(
                frame,
                "QUESTION",
                question,
                final_score,
                question_manager.current_index + 1,
                len(question_manager.questions)
            )

        else:
            draw_ui(frame, "RESULT")

            y_offset = 100

            cv2.putText(frame, "FINAL RESULT", (40, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            for i, (_, score) in enumerate(results_summary):
                cv2.putText(frame, f"Q{i+1}: {score}%", (40, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                y_offset += 30

            if len(results_summary) > 0:
                overall = int(sum([s for _, s in results_summary]) / len(results_summary))

                cv2.putText(frame, f"OVERALL: {overall}%", (40, y_offset+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            if last_question is not None:
                final_score = response_analyzer.get_final_score()
                data_logger.log(last_question, final_score)
                results_summary.append((last_question, final_score))

                response_analyzer.reset()
                last_question = None

    cv2.imshow("AI Deception Analyzer", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


camera.release()
cv2.destroyAllWindows()