import math
import time

import cv2
import mediapipe as mp
import numpy as np

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (0, 0, 255)
BLUE = (245, 117, 25)


def calculate_angle(a, b, c):
    """
    Function to calculate the angle between three points.
    """
    # Convert the points from list or tuple to numpy array
    a = np.array(a)  # First joint coordinate (for example, shoulder)
    b = np.array(b)  # Mid joint coordinate (for example, elbow)
    c = np.array(c)  # End joint coordinate (for example, wrist)

    # Calculate the angle using the atan2 function from the math library
    # The atan2 function returns the angle in radians from the x-axis to the point (y, x),
    # so it's used here to get the angles of the lines bc and ba from the x-axis.
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])

    # Convert the angle from radians to degrees. As we want to get the positive angle,
    # we use the abs function to ensure that the angle is positive.
    angle = np.abs(radians * 180.0 / math.pi)

    # If the calculated angle is more than 180 degrees,
    # then we calculate its supplementary angle by subtracting it from 360 degrees.
    # This is done because the joints can move in any direction and we are interested in the smaller angle formed.
    if angle > 180.0:
        angle = 360 - angle

    return angle


def display_clock_icon(image, icon_path, height, width):
    """
    This function overlays a clock icon on the image.
    :param image: the image on which the clock icon will be overlaid
    :param icon_path: the path to the clock icon
    :param height: the height of the image
    :param width: the width of the image
    :return: the image with the clock icon overlaid
    """
    # Load the clock icon
    clock_icon = cv2.imread(icon_path, -1)

    # Resize the clock icon to desired size
    icon_size = 200  # Change this to the size you want
    clock_icon = cv2.resize(clock_icon, (375, icon_size))

    # Specify the top-right location for the icon (adjust values based on your requirements)
    x_offset = width - clock_icon.shape[1] - 120
    y_offset = 260

    # # If the icon has four channels, perform alpha blending to keep icon transparency
    if clock_icon.shape[2] == 4:
        # Split the icon into its channels and get the alpha channel
        alpha_icon = clock_icon[:, :, 3] / 255.0
        alpha_image = 1.0 - alpha_icon

        for c in range(0, 3):
            # Overlay the clock icon on the image
            image[y_offset:y_offset + clock_icon.shape[0], x_offset:x_offset + clock_icon.shape[1], c] = \
                alpha_icon * clock_icon[:, :, c] + \
                alpha_image * image[y_offset:y_offset + clock_icon.shape[0], x_offset:x_offset + clock_icon.shape[1], c]
    else:
        # If the icon doesn't have an alpha channel, we just overlay it
        image[y_offset:y_offset + clock_icon.shape[0], x_offset:x_offset + clock_icon.shape[1]] = clock_icon

    return image


def display_time(image, start_time, height, width):
    """
    This function displays the elapsed time on the image.
    :param image: the image on which the elapsed time will be displayed
    :param start_time: the time at which the timer started
    :param height: the height of the image
    :param width: the width of the image
    :return: the image with the elapsed time displayed
    """
    elapsed_time = time.time() - start_time

    # Calculate the hours, minutes, seconds and milliseconds from elapsed_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)  # get the milliseconds part

    # Format the elapsed_time string to include milliseconds
    elapsed_time = "{:02}:{:02}:{:02}.{:03}".format(int(hours), int(minutes), int(seconds), milliseconds)

    # Position of the text will be center of the screen on the right side
    position = (int(width / 2 + 200), int(height / 2))

    cv2.putText(image, elapsed_time, position, cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2, cv2.LINE_AA)
    return image


def process_frame(frame, pose):
    """
    Process a frame: convert colorspace, run pose processing, and convert colorspace back.
    :param frame: the frame to process
    :param pose: the pose object
    :return: the processed frame, the pose results, the height and width of the frame
    """

    # Get dimensions of the frame
    height, width, _ = frame.shape

    # Convert the BGR image to RGB.
    # Mediapipe Pose model uses RGB images for processing
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Make the image unwritable as mediapipe pose model requires the input images to be unwritable
    image.flags.writeable = False

    # Process the image to detect pose landmarks
    results = pose.process(image)

    # Make the image writable again so we can draw on it later
    image.flags.writeable = True

    # Convert the image back to BGR for further opencv processing and visualizations
    # Because OpenCV uses BGR as its default color format
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image, results, height, width


def extract_landmarks(results):
    """Extract landmarks (specific body points) from the processed results.
    :param results: the processed results
    :return: the extracted landmarks
    """

    try:
        landmarks = results.pose_landmarks.landmark
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    except:
        pass
    return shoulder, elbow, wrist


def calculate_and_display_angle(shoulder, elbow, wrist, stage, counter):
    """
    Calculate the angle between the shoulder, elbow, and wrist
    :param shoulder: the shoulder landmark
    :param elbow: the elbow landmark
    :param wrist: the wrist landmark
    :param stage: the stage of the rep
    :param counter: the rep counter
    :return: the angle, the stage, and the counter
    """
    angle = calculate_angle(shoulder, elbow, wrist)
    if angle > 160:
        stage = "up"
    if angle < 50 and stage == 'up':
        stage = "down"
        counter += 1
    return angle, stage, counter


def render_ui(image, counter, stage, angle, width):
    """
    Render the frame with the UI elements
    :param image: the image to render
    :param counter: the rep counter
    :param stage: the stage of the rep
    :param angle: the angle between the shoulder, elbow, and wrist
    :param width: the width of the image
    :return: the rendered image
    """
    angle_max = 178  # max angle when arm is fully extended
    angle_min = 25  # min angle when arm is bent

    # Draw the title and background
    cv2.rectangle(image, (int(width / 2) - 150, 0), (int(width / 2) + 250, 73), BLUE, -1)
    cv2.putText(image, 'AI Workout Manager', (int(width / 2) - 100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                WHITE, 2, cv2.LINE_AA)

    # Reps
    cv2.rectangle(image, (0, 0), (255, 73), BLUE, -1)
    cv2.putText(image, 'REPS', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1, cv2.LINE_AA)
    cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2, cv2.LINE_AA)

    # Stage
    cv2.putText(image, 'STAGE', (95, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1, cv2.LINE_AA)
    cv2.putText(image, stage, (95, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2, cv2.LINE_AA)

    # progrss bar
    progress = ((angle - angle_min) / (angle_max - angle_min)) * 100
    cv2.rectangle(image, (50, 350), (50 + int(progress * 2), 370), GREEN, cv2.FILLED)
    cv2.rectangle(image, (50, 350), (250, 370), WHITE, 2)
    cv2.putText(image, f'{int(progress)}%', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2, cv2.LINE_AA)

    return image


def run_pose_detection(mp_drawing, mp_pose, filename):
    """
    Main function to run pose detection and render results.
    mp_drawing: the mediapipe drawing utility
    mp_pose: the mediapipe pose utility
    filename: the filename of the video to process
    return: None
    """
    counter = 0
    stage = None

    # Read video
    cap = cv2.VideoCapture(filename)

    # Start timer
    start_time = time.time()

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while 1:
            ret, frame = cap.read()
            if not ret:
                cap = cv2.VideoCapture('assets/pushup.mp4')
                continue

            # Process frame
            image, results, height, width = process_frame(frame, pose)
            # Extract landmarks
            shoulder, elbow, wrist = extract_landmarks(results)
            # Calculate angle and update stage and counter
            angle, stage, counter = calculate_and_display_angle(shoulder, elbow, wrist, stage, counter)

            # Render UI
            image = render_ui(image, counter, stage, angle, width)

            # Display timer
            image = display_clock_icon(image, 'assets/clock.png', height, width)
            image = display_time(image, start_time, height, width)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=5),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=5))

            # Display the frame
            cv2.imshow('AI Workout Manager', image)

            # Quit when 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        # Release the VideoCapture object
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    """
    Main function to run pose detection and render results.
    """
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    run_pose_detection(mp_drawing, mp_pose, 'assets/pushup.mp4')