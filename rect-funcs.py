import cv2
import numpy as np


def detLen(pts0, pts1):
    xSquared = np.power((pts1[0]-pts0[0]), 2)
    ySquared = np.power((pts1[1]-pts0[1]), 2)
    return np.sqrt((xSquared+ySquared))


def getSecondImage(imageBIN, imageRAW, areaUpper=150000, areaLower=40000):

    kernel = np.ones((5, 5))
    imageDiluted = cv2.dilate(imageBIN, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(imageDiluted, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if contours is not None:
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if areaUpper > area > areaLower:
                polyapp = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
                if len(polyapp) == 4:
                    if polyapp[0, 0, 0] <= polyapp[2, 0, 0]:
                        pts1 = np.float32([polyapp[0, 0], polyapp[1, 0], polyapp[2, 0], polyapp[3, 0]])
                        lineHorizontal = detLen(polyapp[1, 0], polyapp[0, 0])
                        lineVertical = detLen(polyapp[3, 0], polyapp[0, 0])
                    elif polyapp[0, 0, 0] > polyapp[2, 0, 0]:
                        pts1 = np.float32([polyapp[1, 0], polyapp[2, 0], polyapp[3, 0], polyapp[0, 0]])
                        lineHorizontal = detLen(polyapp[2, 0], polyapp[1, 0])
                        lineVertical = detLen(polyapp[0, 0], polyapp[1, 0])

                    if (lineHorizontal * 0.80) < lineVertical < (lineHorizontal * 1.20) or\
                            (lineVertical * 0.80) < lineHorizontal < (lineVertical * 1.20):
                        pts2 = np.float32([[0, 0], [0, 300], [300, 300], [300, 0]])
                        matrix = cv2.getPerspectiveTransform(pts1, pts2)
                        outImage = cv2.warpPerspective(imageRAW, matrix, (300, 300))
                        shapeString = "Square"
                    elif lineHorizontal > lineVertical:
                        pts2 = np.float32([[0, 300], [600, 300], [600, 0], [0, 0]])
                        matrix = cv2.getPerspectiveTransform(pts1, pts2)
                        outImage = cv2.warpPerspective(imageRAW, matrix, (600, 300))
                        shapeString = "Rectangle"
                    elif lineVertical > lineHorizontal:
                        pts2 = np.float32([[0, 0], [0, 300], [600, 300], [600, 0]])
                        matrix = cv2.getPerspectiveTransform(pts1, pts2)
                        outImage = cv2.warpPerspective(imageRAW, matrix, (600, 300))
                        shapeString = "Rectangle"
                    else:
                        outImage = np.zeros((300, 300), np.uint8)
                        shapeString = "Square"

                    return outImage, shapeString
    return None, None
