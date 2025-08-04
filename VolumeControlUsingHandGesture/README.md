# Hand Gesture Volume Control

This project uses computer vision to control your computer's system volume with hand gestures. By tracking your thumb and index finger, the application maps the distance between them to the system's master volume.

## Features
- Real-time hand tracking using MediaPipe.
- Control system volume by adjusting the distance between your thumb and index finger.
- Visual feedback with landmarks and an on-screen volume percentage.
- Real-time FPS display.

## Prerequisites

- **Python 3.6+**
- **A webcam**
- **Windows OS** (The `pycaw` library is specific to Windows for volume control)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TayyabRabbani/Computer-Vision.git
    cd Computer-Vision/VolumeControlUsingHandGesture
    ```

2.  **Create a Python virtual environment** (recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On macOS/Linux, use `source venv/bin/activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the main script:**
    ```bash
    python main.py
    ```
2.  A window will open showing the live feed from your webcam.
3.  Place your hand in view, and the application will track your thumb and index finger.
4.  Increase the distance between your thumb and index finger to raise the volume, and decrease it to lower the volume.
5.  Press `q` to quit the application.