from flask import Flask, Response, render_template, request
import cv2
import mediapipe as mp
import numpy as np
import threading

app = Flask(__name__)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
mp_drawing = mp.solutions.drawing_utils

ARM_LANDMARKS = [
    mp_pose.PoseLandmark.LEFT_SHOULDER,
    mp_pose.PoseLandmark.LEFT_ELBOW,
    mp_pose.PoseLandmark.LEFT_WRIST,
    mp_pose.PoseLandmark.RIGHT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_ELBOW,
    mp_pose.PoseLandmark.RIGHT_WRIST
]

ARM_CONNECTIONS = [
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
    (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
    (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST)
]

start_tracking = False
counter = 0
stage = None
lock = threading.Lock()

cap = cv2.VideoCapture(0)

@app.route('/start_tracking', methods=['POST'])
def handle_start():
    global start_tracking
    start_tracking = True
    return ('', 204)

@app.route('/stop_tracking', methods=['POST'])
def handle_stop():
    global start_tracking
    start_tracking = False
    return ('', 204)

@app.route('/reset_score', methods=['POST'])
def handle_reset():
    global counter, stage
    counter = 0
    stage = None
    return ('', 204)

def calculate_angle(a, b, c):
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return angle

def generate_frames():
    global counter, stage, start_tracking
    while True:
        with lock:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame) if start_tracking else None

            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if start_tracking and results and results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                angle = calculate_angle(shoulder, elbow, wrist)
                
                if angle > 160:
                    stage = "down"
                elif angle < 30 and stage == 'down':
                    stage = "up"
                    counter += 1

                for id, landmark in enumerate(landmarks):
                    if mp_pose.PoseLandmark(id) not in ARM_LANDMARKS:
                        landmark.visibility = 0

                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    ARM_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/get_counter')
def get_counter():
    global counter
    return {'counter': counter}

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html', counter=counter)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
