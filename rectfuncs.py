import cv2
import numpy as np
from math import isclose, atan2, degrees

class rectangle_Mission():
    def rect_side_len(self,arr):
        side_len = list()
        for i in range(len(arr)):
            xSquared = np.power((arr[i][0][0] - arr[0 if i == len(arr)-1 else i+1][0][0]), 2)
            # Calculates x part of pythagoras theorem from 0,1 to 3,0
            ySquared = np.power((arr[i][0][1] - arr[0 if i == len(arr)-1 else i+1][0][1]), 2)
            # Calculates y part of pythagoras theorem from 0,1 to 3,0
            side_len.append(int(np.round(np.sqrt((xSquared+ySquared)))))
            # Uses pythagoras theorem to calculate sides from 0,1 to 3,0 with that order
        return side_len  # Returns side lenghts


    def detLen(self,pts0, pts1):
        xSquared = np.power((pts1[0]-pts0[0]), 2)  # Calculates x part of pythagoras theorem from
        ySquared = np.power((pts1[1]-pts0[1]), 2)  # Calculates y part of pythagoras theorem from
        return np.sqrt((xSquared+ySquared))  # Calculates side lenght from given points and returns it


    def rectCenterCoordinates(self,arr):
        x, y = 0, 0
        for i in range(len(arr)):
            x += arr[i][0][0]  # Adds x part of every corner
            y += arr[i][0][1]  # Adds y part of every corner
        coords = (x/(len(arr)), y/(len(arr)))  # Calculates middle point from given corner points
        return coords  # Returns middle points as ( X , Y )


    def rectLongSideAngle(self,arr):
        if arr[0][0][0] > arr[2][0][0]:  # This is for correction of points if 0 corner is top right corner of rectangle
            arr = arr[3], arr[0], arr[1], arr[2]

        sideA = self.detLen(arr[0][0], arr[1][0])  # Determines upper side length of rectangle
        sideB = self.detLen(arr[0][0], arr[3][0])  # Determines left side length of rectangle

        if sideA > sideB:  # If upper side is bigger side
            radian = atan2((arr[0][0][1] - arr[1][0][1]), (arr[1][0][0] - arr[0][0][0]))  # Calculate angle diff
            degree = degrees(radian)  # Convert angle diff to degrees
        else:  # If left side is bigger than upper side
            if arr[0][0][0] > arr[3][0][0]:  # Correction for corner enum error at some points
                radian = atan2((arr[3][0][1] - arr[0][0][1]), (arr[0][0][0] - arr[3][0][0]))
                degree = degrees(radian)  # Calculate and convert angle diff
            else:
                radian = atan2((arr[3][0][1] - arr[0][0][1]), (arr[3][0][0] - arr[0][0][0]))
                degree = degrees(-1*radian)  # Calculate and convert angle diff

        return degree  # Return angle difference as degrees


    def findRectCenter(self,frame, cannyMin=60, cannyMax=100, dilKernel=5, areaMin=5000, areaMax=500000,
                       arcCoeff=0.02, relTol=0.10):

        frame = cv2.resize(frame, (int(frame.shape[1] * 1.5), int(frame.shape[0] * 1.5)))
        # Use bigger image to detect rectangle

        blurred = cv2.GaussianBlur(frame, (5, 5), 1)  # Gaussion blur to smooth out image
        canny = cv2.Canny(blurred, cannyMin, cannyMax)  # Filter out to binary with canny edge detection

        kernel = np.ones((dilKernel, dilKernel))  # Kernel to dilate binary image
        imageDiluted = cv2.dilate(canny, kernel, iterations=1)  # Dilate binary image with kernel (1 iteration)

        contours, hierarchy = cv2.findContours(imageDiluted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Contour detection with simple chain approx. Do not change retrieval type.

        centerCoords = (None, None)  # Center coordinate holder will return none version if none detected
        angle = None  # Angle detector will return none if none detected
        circumference = None  # Circumference of rectangle

        if contours is not None:  # If there is contour found
            for idx, cnt in enumerate(contours):  # For index, contour in enum(cnts) we want to calculate for every contour
                area = cv2.contourArea(cnt)  # Find contour area
                if areaMin < area < areaMax:  # Limit contours with min and max area limitations
                    poly_approx = cv2.approxPolyDP(cnt, arcCoeff * cv2.arcLength(cnt, True), True)
                    # Approximation of polygon. Arc length can be configured when calling this function
                    if len(poly_approx) == 4:  # Take only quadrilateral shapes
                        side_len = self.rect_side_len(poly_approx)  # Find side lengths of this shape
                        if isclose(side_len[0], side_len[2], rel_tol=0.1) and \
                                isclose(side_len[1], side_len[3], rel_tol=0.1) and \
                                isclose(min(side_len[0], side_len[1]) * 2, max(side_len[0], side_len[1]), rel_tol=relTol):
                            # If shape is rectangle and has x to 2x side lengths
                            centerCoords = self.rectCenterCoordinates(poly_approx)
                            # Find center coordinates of shape
                            centerCoords = (int(centerCoords[0]/1.5), int(centerCoords[1]/1.5))
                            # We made frame 1.5 bigger at start so were making it 1.5 times smaller in coordiantes
                            angle = int(self.rectLongSideAngle(poly_approx))
                            # Find angle of long side
                            circumference = 0
                            for _ in side_len:
                                circumference += _
        return centerCoords, angle, circumference  # Return shape center coordinates and long side angle


    def createMotion(self,rectCoordinates, imageCenter, angle, frameCircumference, rectCircumference, tol=0.05):
        # Create motion if rect center and image center does not match
        if isclose(rectCoordinates[0], imageCenter[0], rel_tol=tol) and\
                isclose(rectCoordinates[1], imageCenter[1], rel_tol=tol) and\
                (-25 < angle < 25):
            # If image center and rect center is within 100*tol % of each other
            # and angle difference is smaller than 25 degrees and
            # rectangle is big enough move forward
            # if rect is not big enough move forward a little and calculate again
            return True
            pass # TODO Create forward motion
        elif isclose(rectCoordinates[0], imageCenter[0], rel_tol=tol) and\
                isclose(rectCoordinates[1], imageCenter[1], rel_tol=tol):
            # If image center and rect center is within 100*tol % of each other
            # but angle difference is too big then fix angle diff issue
            return True
            pass # TODO Decide on what to do if angle doesn't match
        else:
            # If image center and rect center does not match then move to match it
            return False
            pass # TODO Create target locking movement
