import numpy as np
import cv2 as cv

mode = 0

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

    output = None

    if mode == 0:
        output = np.zeros((height * 2, width * 2, channels), 'uint8')
        output[0:height, 0:width, :] = frame[:, :, :]
        output[height:height * 2, 0:width, :] = frame_flipped_y[:, :, :]
        output[0:height, width:width*2, :] = frame_flipped_x[:, :, :]
        output[height:height * 2, width:width*2, :] = frame_flipped_xy[:, :, :]
        output = cv.resize(output, (width, height), interpolation = cv.INTER_AREA)        
    elif mode == 1:        
        output = np.zeros_like(frame)
        output[0:height // 2, 0:width // 2, :] = frame[:height // 2, :width // 2, :]
        output[height // 2:, 0:width // 2, :] = frame_flipped_y[height // 2:, :width // 2, :]
        output[0:height // 2, width // 2:, :] = frame_flipped_x[:height // 2, width // 2:, :]
        output[height // 2:, width // 2:, :] = frame_flipped_xy[height // 2:, width // 2:, :]
    elif mode == 2:
        c1 = cv.addWeighted(frame, 0.5, frame_flipped_y, 0.5,0)
        c2 = cv.addWeighted(frame_flipped_x, 0.5, frame_flipped_xy, 0.5,0)
        output = cv.addWeighted(c1, 0.5, c2, 0.5,0)

    # Display the resulting frame
    cv.imshow('frame', output)
    wait = cv.waitKey(1)
    if wait == ord('q'):
        break
    elif wait == ord('d'):
        mode += 1

        if mode >= 3:
            mode = 0
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
