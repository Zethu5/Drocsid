import uuid
import cv2
import numpy as np
import pyautogui

from features.func import generate_random_path, generate_random_filename, time_prep


def video_record(record_seconds):
    _, time = time_prep(record_seconds)
    file_name = f"{generate_random_path()}{generate_random_filename()}.avi"
    # Display screen resolution
    SCREEN_SIZE = tuple(pyautogui.size())
    # Define the codec (compresses and decompresses digital video)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    frames_per_second = 12.0
    # create the video write object
    out = cv2.VideoWriter(file_name, fourcc, frames_per_second, (SCREEN_SIZE))
    # Keep capturing screenshots and writing to the file in a loop until the seconds are passed
    for i in range(int(time * frames_per_second)):
        # Make a screenshot
        img = pyautogui.screenshot()
        # Convert these pixels to a proper numpy array to work with OpenCV
        frame = np.array(img)
        # Convert colors 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        # if the user clicks q, it exits
        if cv2.waitKey(1) == ord("q"):
            break

    # make sure everything is closed when exited
    cv2.destroyAllWindows()
    out.release()

    return file_name