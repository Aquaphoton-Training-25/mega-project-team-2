import numpy as np
import cv2 
from GroundTruths import GroundTruth

            
class DepthMap(GroundTruth):
    def __init__(self, img_path1='images/bicycle0.png', img_path2='images/bicycle1.png'):
        super().__init__(img_path1)

        self.load_images(img_path1, img_path2)

        #find best matches between the two images
        self.pts0 = []
        self.pts1 = []   
        self.set_matching_points()

        self.set_fundamentalmatrix_and_inlierpoints()

        self.compute_essentialmatrix()

        #decompose the Essential Matrix to obtain rotation and translation
        self.decompose_essentialmatrix()

        #rectify the images and print rectification matrices
        self.rectify_images()

        #find the epipolar lines for both images to check rectification validity
        self.compute_epipolar_lines()

        #draw epipolar lines
        self.draw_epipolar_lines()
        
        #find disparity map (position difference for matching pixels in the two images)
        self.compute_disparity()

        #find the depth map from using the disparity found
        self.compute_depth()


    def load_images(self, path1, path2):
        #load the images
        self.img1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)  
        self.img2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)


    def set_matching_points(self):
        #initialize the SIFT detector
        sift = cv2.SIFT_create()

        #detect keypoints and descriptors
        keypoints1, descriptors1 = sift.detectAndCompute(self.img1, None)
        keypoints2, descriptors2 = sift.detectAndCompute(self.img2, None)

        #initialize the FLANN matcher
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass an empty dictionary
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        #match descriptors
        matches = flann.knnMatch(descriptors1, descriptors2, k=2)

        #ratio test and matching points
        good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

        #extract the matching points
        self.pts1 = np.float32([keypoints1[m.queryIdx].pt for m in good_matches])
        self.pts2 = np.float32([keypoints2[m.trainIdx].pt for m in good_matches])


    def set_fundamentalmatrix_and_inlierpoints(self):
        #estimate the Fundamental Matrix using the RANSAC method
        self.F, mask = cv2.findFundamentalMat(self.pts1, self.pts2, method=cv2.FM_RANSAC)
        # Select inlier points only (if using RANSAC)
        self.pts1_inliers = self.pts1[mask.ravel() == 1]
        self.pts2_inliers = self.pts2[mask.ravel() == 1]

        #SVD to refine the Fundamental matrix 
        U, S, Vt = np.linalg.svd(self.F)
        S[-1] = 0  # enforce rank 2 by setting the smallest singular value to zero
        self.F = np.dot(U, np.dot(np.diag(S), Vt))


    def compute_essentialmatrix(self):
        self.E = np.dot(np.dot(self.K2.T, self.F), self.K1)


    def decompose_essentialmatrix(self):
        _, self.R, self.T, _ = cv2.recoverPose(self.E, self.pts1_inliers, self.pts2_inliers, self.K1)


    def rectify_images(self):
        size = (self.width, self.height)
        #compute the rectification transforms
        self.R1, self.R2, P1, P2, _, _, _ = cv2.stereoRectify(self.K1, None, 
                                                              self.K2, None, 
                                                              size, 
                                                              self.R, self.T, 
                                                              alpha=0, 
                                                              newImageSize=size
                                                             )

        #compute rectification maps
        map1x, map1y = cv2.initUndistortRectifyMap(self.K1, None, self.R1, P1, size, cv2.CV_32FC1)
        map2x, map2y = cv2.initUndistortRectifyMap(self.K2, None, self.R2, P2, size, cv2.CV_32FC1)

        #rectify the images
        self.rectified_img1 = cv2.remap(self.img1, map1x, map1y, cv2.INTER_LINEAR)
        self.rectified_img2 = cv2.remap(self.img2, map2x, map2y, cv2.INTER_LINEAR)

        #print the rectification matrices
        print("Rectification Matrix for Left Image (R1):\n", self.R1, end="\n\n")
        print("Rectification Matrix for Right Image (R2):\n", self.R2, end="\n\n")


    def compute_epipolar_lines(self):
        #compute epipolar lines in the right image for points in the left image
        self.lines1 = cv2.computeCorrespondEpilines(self.pts1_inliers.reshape(-1, 1, 2), 1, self.F)
        self.lines1 = self.lines1.reshape(-1, 3)

        #compute epipolar lines in the left image for points in the right image
        self.lines2 = cv2.computeCorrespondEpilines(self.pts2_inliers.reshape(-1, 1, 2), 2, self.F)
        self.lines2 = self.lines2.reshape(-1, 3)

    
    #epipolar lines should be horizontal on both images
    def draw_epipolar_lines(self):
        img1 = self.rectified_img1
        img2 = self.rectified_img2
        lines1 = self.lines1
        lines2 = self.lines2
        points1 = self.pts1_inliers
        points2 = self.pts2_inliers

        self.img1_epilines = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        self.img2_epilines = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        #draw feature points
        for p1, p2 in zip(points1, points2):
            cv2.circle(self.img1_epilines, tuple(np.int32(p1).tolist()), 5, (0, 255, 0), -1)
            cv2.circle(self.img2_epilines, tuple(np.int32(p2).tolist()), 5, (0, 255, 0), -1)

        #draw epipolar lines on the second image (lines from the first image)
        for line in lines1:
            color = tuple(np.random.randint(0, 255, 3).tolist())
            x0, y0 = map(int, [0, -line[2] / line[1]])
            x1, y1 = map(int, [img2.shape[1], -(line[2] + line[0] * img2.shape[1]) / line[1]])
            cv2.line(self.img2_epilines, (x0, y0), (x1, y1), color, 1)

        #draw epipolar lines on the first image (lines from the second image)
        for line in lines2:
            color = tuple(np.random.randint(0, 255, 3).tolist())
            x0, y0 = map(int, [0, -line[2] / line[1]])
            x1, y1 = map(int, [img1.shape[1], -(line[2] + line[0] * img1.shape[1]) / line[1]])
            cv2.line(self.img1_epilines, (x0, y0), (x1, y1), color, 1)
            


    def compute_disparity(self):
        #set parameters for block matching
        block_size = self.blockSize  #size of the block window for matching
        min_disparity = self.vmin
        num_disparities = self.ndisp  #range of disparities to search
        disparity_range = num_disparities // 16 * 16
        
        # using StereoSGBM to create a disparity map 
        stereo = cv2.StereoSGBM_create(
            minDisparity=min_disparity,
            numDisparities=disparity_range,
            blockSize=block_size,
            P1=8 * 3 * block_size**2,  
            P2=32 * 3 * block_size**2, 
            disp12MaxDiff=1,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=32
        )
        
        #compute the disparity map using the rectified images
        self.disparity = stereo.compute(self.rectified_img1, self.rectified_img2).astype(np.float32) / 16.0
        
        #normalize the disparity map for display
        self.disparity_normalized = cv2.normalize(self.disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        self.disparity_normalized = np.uint8(self.disparity_normalized)
        #covert disparity map to color image
        self.disparitymap_color = cv2.applyColorMap(self.disparity_normalized, cv2.COLORMAP_JET)

        #save the disparity map as grayscale and color image
        cv2.imwrite("task2_outputs/disparitymap_grayscale.png", self.disparity_normalized)
        cv2.imwrite("task2_outputs/disparitymap_color.png", self.disparitymap_color)


    def compute_depth(self):
        #adding small constant to zero disparities to avoid division by zero
        self.disparity = np.float32(self.disparity)
        self.disparity[self.disparity <= 0] = 0.1  

        #compute the depth map
        self.depth_map = (self.focal_length * self.baseline) / (self.disparity)

        #normalize the depth map for display
        self.depthmap_normalized = cv2.normalize(self.depth_map, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        self.depthmap_normalized = np.uint8(self.depthmap_normalized)
        self.depthmap_color = cv2.applyColorMap(self.depthmap_normalized, cv2.COLORMAP_JET)

        #save the depth map as grayscale and color image
        cv2.imwrite("task2_outputs/depth_map_grayscale.png", self.depthmap_normalized)
        cv2.imwrite("task2_outputs/depth_map_color.png", self.depthmap_color)


    def calculate_length(self, point1, point2):
        x1, y1 = point1.x(), point1.y() #QPoint
        x2, y2 = point2.x(), point2.y() #QPoint

        d1 = self.depth_map[y1, x1]
        d2 = self.depth_map[y2, x2]

        fx, fy = self.focal_length, self.focal_length

        cx1, cy1 = self.K1[0, 2], self.K1[1, 2]
        cx2, cy2 = self.K2[0, 2], self.K2[1, 2]

        #calculate 3D coordinates
        X1, Y1, Z1 = (x1 - cx1) * d1 / fx, (y1 - cy1) * d1 / fy, d1
        X2, Y2, Z2 = (x2 - cx2) * d2 / fx, (y2 - cy2) * d2 / fy, d2

        #compute the Euclidean distance between the two points
        return np.sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)


    



    


