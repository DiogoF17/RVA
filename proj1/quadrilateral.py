import cv2 as cv
class Quadrilateral:
    def __init__(self, centroid, contours, verticesCoords):
        self.centroid = centroid
        self.contours = contours
        self.verticesCoords = verticesCoords
        self.homography = None
        self.width, self.height = self.computeDimensions()

    def computeDimensions(self):
        _, _, width, height = cv.boundingRect(self.contours)
        return width, height