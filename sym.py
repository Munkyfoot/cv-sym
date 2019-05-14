import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    height, width, channels = frame.shape

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame_flipped_y = np.flip(frame, 0)
    frame_flipped_x = np.flip(frame, 1)
    frame_flipped_xy = np.flip(frame_flipped_y, 1)

    output = np.zeros((height * 2, width * 2, channels), 'uint8')
    output[0:height, 0:width, :] = frame[:, :, :]
    output[height:height * 2, 0:width, :] = frame_flipped_y[:, :, :]
    output[0:height, width:width*2, :] = frame_flipped_x[:, :, :]
    output[height:height * 2, width:width*2, :] = frame_flipped_xy[:, :, :]

    # Display the resulting frame
    cv.imshow('frame', output)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
