import cv2
import numpy as np
from math import isclose
from rectfuncs import rect_side_len


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_COUNT, 30)

while cap.isOpened():
    ret, frame = cap.read()

    blurred = cv2.GaussianBlur(frame, (5, 5), 1)
    canny = cv2.Canny(blurred, 120, 180)

    kernel = np.ones((5, 5))
    imageDiluted = cv2.dilate(canny, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(imageDiluted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours is not None:
        for idx, cnt in enumerate(contours):
            drawFlag = False
            area = cv2.contourArea(cnt)
            if 5000 < area < 500000:
                poly_approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
                if len(poly_approx) == 4:
                    side_len = rect_side_len(poly_approx)
                    if isclose(side_len[0], side_len[2], rel_tol=0.1) and\
                            isclose(side_len[1], side_len[3], rel_tol=0.1) and\
                            isclose(min(side_len[0],side_len[1])*2, max(side_len[0],side_len[1]), rel_tol=0.10):
                        drawFlag = True
                        #TODO find angle of long side
            if drawFlag:
                cv2.drawContours(frame, contours, idx, (0, 255, 255), 2)

    cv2.imshow("Original", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
