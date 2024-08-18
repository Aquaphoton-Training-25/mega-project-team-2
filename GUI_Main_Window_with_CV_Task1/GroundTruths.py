import numpy as np


class GroundTruth():
    def __init__(self, flag):
        if "bicycle" in flag:
            self.K1 = np.array([[5299.313, 0, 1263.818],#intrinsic parameters for camera {0} 
                    [0, 5299.313, 977.763],
                    [0, 0, 1]])

            self.K2 = np.array([[5299.313, 0, 1438.004],#intrinsic parameters for camera {1} 
                    [0, 5299.313, 977.763],
                    [0, 0, 1]]) 
                
            self.width = 2988 #image width
            self.height = 2008 #image hight
            self.baseline = 177.288/1000 #distance between the two cameras(converted from mm to m)
            self.focal_length = 5299.313 #focal length in pixels (for both cameras)
            self.doffs = 174.186 #difference of principle points
            self.ndisp = 180 #disparity levels
            self.vmin = 54 #minimum disparity
            self.blockSize = 5

        elif "toys" in flag:
            self.K1 = np.array([[4396.869, 0, 1353.072],
                            [0, 4396.869, 989.702],
                            [0, 0, 1]])

            self.K2 = np.array([[4396.869, 0, 1543.51],
                                [0, 4396.869, 989.702],
                                [0, 0, 1]]) 
                    
            self.width = 2880 
            self.height = 1980 
            self.baseline = 144.049/1000 
            self.focal_length = 4396.869 
            self.doffs = 185.788 
            self.ndisp = 640 
            self.vmin = 17 
            self.blockSize = 5
        
        elif "ubrella" in flag:
            self.K1 = np.array([[5806.559, 0, 1429.219],
                    [0, 5806.559, 993.403],
                    [0, 0, 1]])

            self.K2 = np.array([[5806.559, 0, 1438.004],
                    [0, 5806.559, 993.403],
                    [0, 0, 1]]) 
                
            self.width = 2960 
            self.height = 2016 
            self.baseline = 174.019/1000 
            self.focal_length = 5806.559 
            self.doffs = 114.291 
            self.ndisp = 250
            self.vmin = 38
            self.blockSize = 11