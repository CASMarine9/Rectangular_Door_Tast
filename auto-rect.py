import cv2
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_COUNT, 30)

while cap.isOpened():
    ret, frame = cap.read()

    # blurred = cv2.GaussianBlur(frame, (5, 5), 1)
    # canny = cv2.Canny(blurred, 60, 100)
    # kernel = np.ones((5, 5), np.uint8)
    # canny = cv2.dilate(canny, kernel, iterations=2)
    # canny = cv2.erode(canny, kernel, iterations=1)

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
