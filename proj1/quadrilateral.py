class Quadrilateral:
    def __init__(self, centroid, contours, verticesCoords):
        self.centroid = centroid
        self.contours = contours
        self.verticesCoords = verticesCoords
        self.homography = None
