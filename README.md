# Realtime Gym Workout Tracker
## Realtime workout tracker using **OpenCv** and **MediaPipe**

- A Bicep curl counter is built using `OpenCv` and `MediaPipe` in python
- We estimate the joint cordinates and calculate angles between joints
- Then we setup a counter for motion of bicep curl based on angles between the joints.

_More workouts to be added..._

# AI Workout Manager

The AI Workout Manager is a pose detection application that uses Python, OpenCV, and MediaPipe to count exercise reps. It's capable of identifying different stages of reps and can calculate angles between various body landmarks during the workout.

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

The AI Workout Manager relies on the following libraries:

- OpenCV for image and video processing.
- MediaPipe for pose detection.
- Numpy for numerical operations.
- Math and time libraries from Python's standard library.

## Usage

You can run the AI Workout Manager by using the following command:

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

If you have any questions or suggestions, please feel free to write me an email at airscholar@gmail.com.
