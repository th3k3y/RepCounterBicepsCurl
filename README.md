# RepCounter

This project is a web-based application utilizing Flask to create a Pose Estimation API. It leverages OpenCV for video processing and MediaPipe for pose estimation, particularly focusing on arm movements. The application tracks the arm's angle and counts movements, which could be used for various purposes like monitoring exercise movements (e.g., bicep curls).

![Alt text]([URL_of_GIF](https://github-production-user-asset-6210df.s3.amazonaws.com/49789253/302063395-fbc9ff29-3b2a-492b-b2fe-608d31e5c5b6.gif?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20240203%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240203T213321Z&X-Amz-Expires=300&X-Amz-Signature=646ed4a71493886327e59cbb9fdb56ab7ed63b3e664c1b745cea4b467150f91b&X-Amz-SignedHeaders=host&actor_id=49789253&key_id=0&repo_id=752445152))

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
