import cv2
import numpy as np
import math

arra = np.array([[[503, 170]], [[690, 175]], [[688, 263]], [[501, 260]]])

def rect_side_len(arr):
    side_len = list()
    for i in range(len(arr)):
        xSquared = np.power((arr[i][0][0] - arr[0 if i == len(arr)-1 else i+1][0][0]), 2)
        ySquared = np.power((arr[i][0][1] - arr[0 if i == len(arr)-1 else i+1][0][1]), 2)
        side_len.append(int(np.round(np.sqrt((xSquared+ySquared)))))
    return side_len

a = 90
b = 80

x = [1,2,3,4]

f = 0

for _ in x:
    f += _

print(math.isclose(a,b,rel_tol=0.1, abs_tol=0))
print(math.atan2(-2,3))
print(f)
