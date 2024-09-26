const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');
const counterElement = document.getElementById('counter');

let startTracking = false;
let counter = 0;
let stage = null;


function calculateAngle(a, b, c) {
    let radians = Math.atan2(c.y - b.y, c.x - b.x) - Math.atan2(a.y - b.y, a.x - b.x);
    let angle = Math.abs(radians * 180.0 / Math.PI);
    if (angle > 180.0) {
        angle = 360 - angle;
    }
    return angle;
}

function onResults(results) {
    if (!results.poseLandmarks) {
        return;
    }

    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

    if (startTracking) {
        const landmarks = results.poseLandmarks;
        const shoulder = landmarks[11];
        const elbow = landmarks[13];
        const wrist = landmarks[15];

        const angle = calculateAngle(shoulder, elbow, wrist);

        if (angle > 160) {
            stage = "down";
        } else if (angle < 30 && stage === 'down') {
            stage = "up";
            counter++;
            counterElement.textContent = `Score: ${counter}`;
        }

        // Draw pose landmarks
        drawConnectors(canvasCtx, landmarks, POSE_CONNECTIONS, {color: '#00FF00', lineWidth: 4});
        drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2});
    }

    canvasCtx.restore();
}

const pose = new Pose({locateFile: (file) => {
    return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
}});
pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});
pose.onResults(onResults);

const camera = new Camera(videoElement, {
    onFrame: async () => {
        await pose.send({image: videoElement});
    },
    width: 1280,
    height: 720
});
camera.start().then(() => {
    console.log("Camera started successfully");
}).catch((error) => {
    console.error("Error starting camera:", error);
});

document.getElementById('startBtn').addEventListener('click', () => {
    startTracking = true;
});

document.getElementById('stopBtn').addEventListener('click', () => {
    startTracking = false;
});

document.getElementById('resetBtn').addEventListener('click', () => {
    counter = 0;
    stage = null;
    counterElement.textContent = `Score: ${counter}`;
});
