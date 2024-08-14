import numpy as np
import cv2
import imutils

def read_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def preprocess_image(image):
    # Split the image into its color channels
    channels = cv2.split(image)
    
    # Create a CLAHE object
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    
    # Apply CLAHE to each channel
    equalized_channels = [clahe.apply(channel) for channel in channels]
    
    # Merge the channels back together
    equalized_image = cv2.merge(equalized_channels)
    
    return equalized_image

def compute_homography_matrix(frame1, frame2):
    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Find keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(frame1, None)
    kp2, des2 = orb.detectAndCompute(frame2, None)

    # Create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance
    matches = sorted(matches, key = lambda x:x.distance)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = kp1[match.queryIdx].pt
        points2[i, :] = kp2[match.trainIdx].pt

    # Find homography matrix
    H, mask = cv2.findHomography(points2, points1, cv2.RANSAC)

    return H

def stitch_videos(video1_frames, video2_frames):
    if len(video1_frames) != len(video2_frames):
        raise ValueError("The videos must have the same number of frames.")

    if video1_frames[0].shape != video2_frames[0].shape:
        raise ValueError("Frames from both videos must have the same dimensions.")

    stitched_frames = []
    homography_matrix = None

    for i, (frame1, frame2) in enumerate(zip(video1_frames, video2_frames)):
        frame1 = preprocess_image(frame1)
        frame2 = preprocess_image(frame2)

        if i == 0:
            # Compute the homography matrix from the first frame
            homography_matrix = compute_homography_matrix(frame1, frame2)
            if homography_matrix is None:
                print(f"Frames {i} could not be stitched due to no homography found.")
                stitched_frames.append(frame1)
            else:
                stitched_img = cv2.warpPerspective(frame2, homography_matrix, (frame1.shape[1], frame1.shape[0]))
                stitched_img = np.maximum(frame1, stitched_img)
                stitched_frames.append(stitched_img)
        else:
            # Apply the homography matrix to subsequent frames
            if homography_matrix is not None:
                warped_frame2 = cv2.warpPerspective(frame2, homography_matrix, (frame1.shape[1], frame1.shape[0]))
                stitched_img = np.maximum(frame1, warped_frame2)
                stitched_frames.append(stitched_img)
            else:
                print(f"Frames {i} could not be stitched as homography is not available.")
                stitched_frames.append(frame1)

    return stitched_frames

def resize_frames(frames, target_size):
    resized_frames = []
    for frame in frames:
        if frame is not None and frame.size > 0:
            resized_frame = cv2.resize(frame, target_size)
            resized_frames.append(resized_frame)
    return resized_frames

def save_video(frames, output_path, frame_rate):
    if frames:
        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, frame_rate, (width, height))

        if not out.isOpened():
            raise ValueError("Could not open video writer.")
        
        for i, frame in enumerate(frames):
            if frame is None or frame.size == 0:
                print(f"Frame {i} is empty or None.")
                continue

            if frame.shape[:2] != (height, width):
                print(f"Resizing frame {i} from {frame.shape[:2]} to {(height, width)}")
                frame = cv2.resize(frame, (width, height))

            out.write(frame)
            print(f"Writing frame {i}")

        out.release()
    else:
        raise ValueError("No frames to write.")

if __name__ == '__main__':
    video1_path = "C:\\Users\\HP ENVY\\Downloads\\Right(Better Quality).mp4"
    video2_path = "C:\\Users\\HP ENVY\\Downloads\\Left (Better Quality).mp4"
    output_path = r"C:\Users\HP ENVY\Downloads\stitched (Better Quality).avi"

    video1_frames = read_video_frames(video1_path)
    video2_frames = read_video_frames(video2_path)
    
    if len(video1_frames) != len(video2_frames):
        raise ValueError("The videos must have the same number of frames.")

    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)
    frame_rate1 = cap1.get(cv2.CAP_PROP_FPS)
    frame_rate2 = cap2.get(cv2.CAP_PROP_FPS)
    cap1.release()
    cap2.release()

    if frame_rate1 != frame_rate2:
        raise ValueError("Both videos must have the same frame rate.")

    stitched_frames = stitch_videos(video1_frames, video2_frames)
    if stitched_frames:
        height, width = stitched_frames[0].shape[:2]
        resized_frames = resize_frames(stitched_frames, (width, height))
        save_video(resized_frames, output_path, frame_rate1)

    print(f"Stitched video saved to {output_path}")
