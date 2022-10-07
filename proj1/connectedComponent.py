class ConnectedComponent:
    def __init__(self, mask, centroid):
        self.mask = mask
        self.centroid = (int(centroid[0]),int(centroid[1]))
