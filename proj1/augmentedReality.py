import cv2 as cv
import numpy as np

# =============================GLOBAL VARIABLES================================

REAL_MARKER_COORDS = np.float32([[0, 0, 0],[1, 0, 0],[1, 1, 0],[0, 1, 0]])

CUBE_VERTICES = np.float32([[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0],
                   [0, 0, -1], [0, 1, -1], [1, 1, -1], [1, 0, -1] ])

# Load calibration data
with np.load('camera/calibration/calibrationData.npz') as X:
    MTX, DIST = [X[i] for i in ('mtx','dist')]

# ===============================FUNCTIONS=====================================

def detectMarker(img):
    arucoDict = cv.aruco.Dictionary_get(cv.aruco.DICT_ARUCO_ORIGINAL)
    arucoParams = cv.aruco.DetectorParameters_create()
    (corners, _, _) = cv.aruco.detectMarkers(img, arucoDict, parameters = arucoParams)

    if len(corners) == 0:
        return []

    return np.float32(corners)[0, 0, :]

def poseEstimation(imageMarkerCoords):

    # Find the rotation and translation vectors.
    _, rvecs, tvecs = cv.solvePnP(REAL_MARKER_COORDS, imageMarkerCoords, MTX, DIST)

    return rvecs,tvecs

def augment(img, rvecs, tvecs):
    # project 3D cube points to image plane
    imgpts, _ = cv.projectPoints(CUBE_VERTICES, rvecs, tvecs, MTX, DIST)
    imgpts = np.int32(imgpts).reshape(-1,2)

    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    
    # draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)
    
    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), 3)


# image = cv.imread("camera/calibration/images/IMG_20221016_105437.jpg")

# h,w,_ = image.shape

# (H, _) = cv.findHomography(np.array([[0,0],[0,w],[h,w],[h,0]]), imgpts[4:])
# warped = cv.warpPerspective(image, H, (img.shape[1], img.shape[0]))
# cv.imshow("warped",warped)

def showTrophy(frame):
    imageMarkerCoords = detectMarker(frame)

    if len(imageMarkerCoords) != 0:
        rvecs, tvecs = poseEstimation(imageMarkerCoords)

        augment(frame, rvecs, tvecs)