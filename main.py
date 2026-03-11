import os
import cv2
import numpy as np
from computer_vision.frame_extractor import extract_frames
from computer_vision.detection_engine import detect_people
from computer_vision.object_tracker import SimpleTracker
from event_engine.event_detector import detect_events
from agents.vision_agent import vision_agent
from agents.context_agent import context_agent
from agents.decision_agent import decision_agent
from agents.alert_agent import alert_agent

# 1. Setup Dummy Environment (For testing if no real video or model exists)
video_path = "data/videos/test_video.mp4"
os.makedirs("data/videos", exist_ok=True)
os.makedirs("models", exist_ok=True)

if not os.path.exists(video_path):
    print("Creating a dummy test video for extraction...")
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1.0, (640, 480))
    for i in range(5): 
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, f"Test Frame {i}", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        out.write(frame)
    out.release()

# Dummy model class for testing without the real 16MB pytorch model
class DummyModel:
    def __init__(self):
        pass
    def eval(self):
        pass
    def __call__(self, frame):
        # Fake 6 detections to trigger the crowd event (>5)
        return [
            {"bbox": [10, 10, 50, 50], "score": 0.95},
            {"bbox": [60, 60, 100, 100], "score": 0.92},
            {"bbox": [110, 110, 150, 150], "score": 0.88},
            {"bbox": [160, 160, 200, 200], "score": 0.85},
            {"bbox": [210, 210, 250, 250], "score": 0.91},
            {"bbox": [260, 260, 300, 300], "score": 0.89}
        ]

# 2. Extract Frames
print("--- Extracting Frames ---")
extract_frames(video_path, "data/frames")

# 3. Initialize Components
print("\n--- Initializing AI Surveillance System ---")
model = DummyModel() # Replace with actual load_model("models/people_detection.pt")
model.eval()

tracker = SimpleTracker()

# 4. Process Workflow
print("\n--- Running AI Pipeline ---")
# Simulating processing frame 0
frame_path = "data/frames/frame_0.jpg"
frame = cv2.imread(frame_path)

if frame is not None:
    # PyTorch Detection
    detections = detect_people(model, frame)
    print(f"Detected {len(detections)} people.")
    
    # Object Tracking
    tracks = tracker.update(detections, frame_id=0)
    
    # Event Detection
    events = detect_events(detections)
    
    # Multi-Agent AI Processing
    for event_data in events:
        event_name = event_data["event"]
        print(f"\nProcessing Event: {event_name}")
        
        # Agents processing
        v_context = vision_agent(event_name)
        policy_context = context_agent(event_name)
        risk_level = decision_agent(event_name)
        
        print(f"Vision Context: {v_context}")
        print(f"Policy Context: {policy_context}")
        
        # Trigger Alert
        alert_agent(event_name, risk_level)
else:
    print("Error loading frame.")
