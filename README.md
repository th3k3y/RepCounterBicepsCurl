# RepCounter

This project is a web-based application utilizing Flask to create a Pose Estimation API. It leverages OpenCV for video processing and MediaPipe for pose estimation, particularly focusing on arm movements. The application tracks the arm's angle and counts movements and especially biceps curl repetitions.

![screencapture-localhost-5000-2024-02-03-22_36_21](https://github.com/th3k3y/RepCounterBicepsCurl/assets/49789253/3033e516-ef54-4927-866a-8d9eb7e4c35a)

## Features

- Real-time video streaming and pose estimation.
- Arm movement tracking with angle calculation.
- Counting the number of complete movements.
- Start, stop, and reset functionalities through web endpoints.

## How It Works

The application uses a Flask server to handle requests and serve a webpage for the user interface. It captures video frames from the user's webcam, processes them using OpenCV, and then applies MediaPipe's pose estimation. The angle of the arm is calculated, and movements are counted based on the angle thresholds.

## Endpoints

- `/start_tracking`: Initiates the pose tracking.
- `/stop_tracking`: Stops the pose tracking.
- `/reset_score`: Resets the counter to 0.
- `/get_counter`: Retrieves the current counter value.
- `/video_feed`: Streams the video feed with pose estimation overlay.
- `/`: The main index page showing the interface and the counter.

## Setup and Installation

Ensure you have Python 3.x installed. Then, install the required libraries:

```bash
pip install Flask opencv-python-headless mediapipe numpy
