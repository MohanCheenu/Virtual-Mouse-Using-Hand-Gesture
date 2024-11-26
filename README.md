# Hand Gesture Control for Mouse Interaction

This project allows users to control the mouse cursor and perform left/right clicks using hand gestures. It uses OpenCV for real-time video capture, MediaPipe for hand gesture recognition, and PyAutoGUI for mouse control. By recognizing specific hand gestures like "pinch" and "double-finger," the program simulates mouse actions.

## Features

- **Hand Gesture Recognition**: Detects and interprets hand gestures using MediaPipe.
- **Mouse Movement**: Controls the mouse cursor position based on hand gestures.
- **Left Click (Pinch Gesture)**: Simulates a left-click when a pinch gesture (thumb and index finger close) is detected.
- **Right Click (Double Finger Gesture)**: Simulates a right-click when the index and middle fingers are close together.
- **Real-time Processing**: Captures video frames in real-time using OpenCV and processes hand gestures.

## Requirements

- OpenCV (opencv-python): Used for real-time video capture, image processing, and displaying the video frames.
  ```bash
  pip install opencv-python
- MediaPipe (mediapipe): Used for hand gesture recognition and hand tracking.
  ```bash
  pip install mediapipe
- PyAutoGUI (pyautogui): Used for controlling the mouse, including moving the cursor and simulating mouse clicks.
  ```bash
  pip install pyautogui
### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/hand-gesture-control.git
   cd hand-gesture-control
