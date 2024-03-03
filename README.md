# Realtime Gym Workout Tracker

The Gym Workout Tracker is a pose detection application that uses Python, OpenCV, and MediaPipe to count exercise reps and estimate posture. It's capable of identifying different stages of reps and can calculate angles between various body landmarks during different workouts like bicep curls, pushups etc.

## Features

- Real-time pose detection.
- Exercise repetition counting.
- Visual interface with performance metrics.
- Elapsed time tracking.

## Installation

Make sure you have Python 3 installed. Then, clone the repository and install the necessary packages:

```bash
git clone https://github.com/airscholar/AI-Workout-Manager.git
cd AI-Workout-Manager
pip install -r requirements.txt
```

## Dependencies

The Gym Workout Tracker relies on the following libraries:

- `OpenCV` for image and video processing.
- `MediaPipe` for pose detection.
- `Numpy` for numerical operations.
- `Math` and `time` libraries from Python's standard library.

## Usage

You can run the Gym Workout Manager by using the following command:

```bash
python main.py
```

## File Structure

The main code is in the root directory:

- `main.py`: The primary script containing the application's logic.

The assets directory contains any external assets, like videos or images, that the program uses:

- `pushup.mp4`: An example video file of a person doing pushups.
- `clock.png`: A clock icon used in the UI.

## Contact

If you have any questions or suggestions, please feel free to write me an email at tvrraviteja@gmail.com.
