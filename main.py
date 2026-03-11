import os
from computer_vision.frame_extractor import extract_frames

# Create dummy video for testing if it doesn't exist
video_path = "data/videos/test_video.mp4"
os.makedirs("data/videos", exist_ok=True)

if not os.path.exists(video_path):
    print("Creating a dummy test video for extraction...")
    import cv2
    import numpy as np
    
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1.0, (640, 480))
    for i in range(5): # Create 5 frames
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, f"Test Frame {i}", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        out.write(frame)
    out.release()

extract_frames(
    video_path,
    "data/frames"
)
