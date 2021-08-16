import cv2
import rectfuncs


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_COUNT, 30)
cla = rectfuncs.rectangle_Mission()

while cap.isOpened():
    ret, frame = cap.read()
    frame = frame[120:600, 280:1000]
    centerCoord = [int(frame.shape[1]/2), int(frame.shape[0]/2)]
    frameCircumference = (int(frame.shape[1]/2) + int(frame.shape[0]/2))*2

    coordinates, angle, rectCircumference = cla.findRectCenter(frame)

    if (coordinates[0] and coordinates[1] and angle) is not None:
        flag = cla.createMotion(coordinates, centerCoord, angle, frameCircumference, rectCircumference, tol=0.15) # TODO Complete motion function
        if flag:
            cv2.circle(frame,(coordinates[0], coordinates[1]), 10, (0, 255, 0), cv2.FILLED) # This draws coord to image
        else:
            cv2.circle(frame, (coordinates[0], coordinates[1]), 10, (123, 0, 255), cv2.FILLED)  # This draws coord to image

    cv2.imshow("Original", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
