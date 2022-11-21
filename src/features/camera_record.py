import cv2

from features.func import generate_random_filename, generate_random_path, time_prep


def camrecord(time):
    _, record_seconds = time_prep(time)
    frames_per_second = 12.0
    vid_capture = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not vid_capture.isOpened():
        raise IOError("Cannot open webcam")

    # Create a file “.avi” and write in this file.
    random_path = generate_random_path() + generate_random_filename() + ".avi"
    print(f"recording to: {random_path}")

    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter(random_path, vid_cod, 20.0, (640,480))

    for i in range(int(record_seconds * frames_per_second)):
        ret,frame = vid_capture.read()
        output.write(frame)
        if cv2.waitKey(1) &0XFF == ord('q'):
            break
    # Close the already opened camera
    vid_capture.release()
    # Close the already opened file
    output.release()
    # Close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

    return random_path