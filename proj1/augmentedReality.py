import cv2 as cv
import numpy as np

# =============================GLOBAL VARIABLES================================

REAL_MARKER_COORDS = np.float32([[0, 0, 0],[1, 0, 0],[1, 1, 0],[0, 1, 0]])

CUBE_VERTICES = np.float32([[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0],
                   [0, 0, -1], [0, 1, -1], [1, 1, -1], [1, 0, -1] ])

# Load calibration data
with np.load('camera/calibration/calibrationData.npz') as X:
    MTX, DIST = [X[i] for i in ('mtx','dist')]

WINNER_PHOTOS = [cv.imread(f"winnerPhotos/winner{i}.jpg") for i in range(0, 3)]

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

    return rvecs, tvecs

def augment(img, winner, rvecs, tvecs):
    # project 3D cube points to image plane
    imgpts, _ = cv.projectPoints(CUBE_VERTICES, rvecs, tvecs, MTX, DIST)
    imgpts = np.int32(imgpts).reshape(-1, 2)

    drawTrophy(img, imgpts)
    return drawWinnerPhoto(img, winner, imgpts[4:])

def drawWinnerPhoto(img, winner, topCubeFace):
    h,w,_ = WINNER_PHOTOS[winner].shape

    (H, _) = cv.findHomography(np.array([[0,0],[0,h],[w,h],[w,0]]), topCubeFace)
    warped = cv.warpPerspective(WINNER_PHOTOS[winner], H, (img.shape[1], img.shape[0]))

    mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")
    cv.fillConvexPoly(mask, topCubeFace.astype("int32"), (255, 255, 255), cv.LINE_AA)

    maskScaled = mask.copy() / 255.0
    maskScaled = np.dstack([maskScaled] * 3)

    warpedMultiplied = cv.multiply(warped.astype("float"), maskScaled)
    imageMultiplied = cv.multiply(img.astype(float), 1.0 - maskScaled)
    output = cv.add(warpedMultiplied, imageMultiplied).astype("uint8")

    return output

def drawTrophy(img, imgpts):
    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)
    
    # draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)
    
    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), 3)

def showTrophy(frame, winner):
    imageMarkerCoords = detectMarker(frame)

    if len(imageMarkerCoords) != 0:
        rvecs, tvecs = poseEstimation(imageMarkerCoords)

        return augment(frame, winner, rvecs, tvecs)

    return frame