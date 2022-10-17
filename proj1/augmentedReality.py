# import cv2 as cv
# import camera.remoteWebCam as remoteWebCamPackage
# import numpy as np


# def detectMarker(img):
#     arucoDict = cv.aruco.Dictionary_get(cv.aruco.DICT_ARUCO_ORIGINAL)
#     arucoParams = cv.aruco.DetectorParameters_create()
#     (corners, _, _) = cv.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)

#     if len(corners) == 0:
#         return []

#     return np.float32(corners)[0,0,:]

# def poseEstimation(imageMarkerCoords, realMarkerCoords, mtx, dist):

#     # Find the rotation and translation vectors.
#     _, rvecs, tvecs = cv.solvePnP(realMarkerCoords, imageMarkerCoords, mtx, dist)

#     return rvecs,tvecs

# def augment(img, axis, rvecs, tvecs, mtx, dist):
#     # project 3D points to image plane
#     imgpts, _ = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)

#     imgpts = np.int32(imgpts).reshape(-1,2)

#     # draw ground floor in green
#     img = cv.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    
#     # draw pillars in blue color
#     for i,j in zip(range(4),range(4,8)):
#         img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
    
#     # draw top layer in red color
#     img = cv.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)


# camera = remoteWebCamPackage.RemoteWebCam()

# axis = np.float32([[0,0,0], [0,1,0], [1,1,0], [1,0,0],
#                    [0,0,-1],[0,1,-1],[1,1,-1],[1,0,-1] ])

# # Load previously saved data
# with np.load('camera/calibration/calibrationData.npz') as X:
#     mtx, dist = [X[i] for i in ('mtx','dist')]

# while True:
#     camera.nextFrame()
#     if not camera.validFrame():
#         print("Couldn't get video from camera")
#         print("Exiting...")
#         break
    
#     frame = camera.getFrame()
    
#     realMarkerCoords = np.float32([[0,0,0],[1,0,0],[1,1,0],[0,1,0]])
#     imageMarkerCoords = detectMarker(frame)

#     for coords in imageMarkerCoords:
#         cv.circle(frame, np.int0(coords), 5, (0,0,255), -1)

#     if len(imageMarkerCoords) != 0:
#         rvecs, tvecs = poseEstimation(imageMarkerCoords,realMarkerCoords, mtx, dist)

#         augment(frame, axis, rvecs, tvecs, mtx, dist)
    
#     cv.imshow("video", frame)
    
#     key = cv.waitKey(1)
#     if key == ord("q"):
#         break
    
# cv.destroyAllWindows()


import cv2 as cv
import camera.remoteWebCam as remoteWebCamPackage
import numpy as np

# =============================GLOBAL VARIABLES================================

REAL_MARKER_COORDS = np.float32([[0,0,0],[1,0,0],[1,1,0],[0,1,0]])

CUBE_VERTICES = np.float32([[0,0,0], [0,1,0], [1,1,0], [1,0,0],
                   [0,0,-1],[0,1,-1],[1,1,-1],[1,0,-1] ])

# Load previously saved data
with np.load('camera/calibration/calibrationData.npz') as X:
    MTX, DIST = [X[i] for i in ('mtx','dist')]

# ===============================FUNCTIONS=====================================

def detectMarker(img):
    arucoDict = cv.aruco.Dictionary_get(cv.aruco.DICT_ARUCO_ORIGINAL)
    arucoParams = cv.aruco.DetectorParameters_create()
    (corners, _, _) = cv.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)

    if len(corners) == 0:
        return []

    return np.float32(corners)[0,0,:]

def poseEstimation(imageMarkerCoords):

    # Find the rotation and translation vectors.
    _, rvecs, tvecs = cv.solvePnP(REAL_MARKER_COORDS, imageMarkerCoords, MTX, DIST)

    return rvecs,tvecs

def augment(img, rvecs, tvecs):
    # project 3D points to image plane
    imgpts, _ = cv.projectPoints(CUBE_VERTICES, rvecs, tvecs, MTX, DIST)

    imgpts = np.int32(imgpts).reshape(-1,2)

    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    
    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
    
    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)


def showTrophy(frame):
    imageMarkerCoords = detectMarker(frame)

    if len(imageMarkerCoords) != 0:
        rvecs, tvecs = poseEstimation(imageMarkerCoords)

        augment(frame, rvecs, tvecs)