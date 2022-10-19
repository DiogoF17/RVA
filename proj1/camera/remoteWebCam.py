import requests
import numpy as np
import cv2 as cv

class RemoteWebCam:
    def __init__(self):
        self.url = self.getCameraUrl()
        print("\n+++++++++++++++++++++++++++++++++++++++++++\n")
        
    def getCameraUrl(self):
        url = input("Camera URL: ")
        return "http://" + url + "/shot.jpg"
    
    def nextFrame(self):
        self.frame = requests.get(self.url)
    
    def getFrame(self):            
        frame_arr = np.array(bytearray(self.frame.content), dtype=np.uint8)
        frame = cv.imdecode(frame_arr, -1)
        width, height = 750, 500
        frame = cv.resize(frame, (width, height), cv.INTER_AREA)
        
        return frame
        
    def validFrame(self):
        if self.frame.status_code == 200:
            return True
        else:
            return False