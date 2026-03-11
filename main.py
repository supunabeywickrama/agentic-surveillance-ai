import os
import cv2
import time
import numpy as np
from computer_vision.frame_extractor import extract_frames
from computer_vision.detection_engine import detect_people
from computer_vision.object_tracker import AdvancedTracker
from event_engine.event_detector import EventDetector
from agents.langgraph_setup import build_surveillance_graph

# Setup Dummy Video
video_path = "data/videos/test_video.mp4"
os.makedirs("data/videos", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("data/processed/reports", exist_ok=True)

if not os.path.exists(video_path):
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1.0, (640, 480))
    for i in range(5): 
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, f"Test Frame {i}", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        out.write(frame)
    out.release()

class DummyModel:
    def eval(self): pass
    def __call__(self, frame):
        return [
            {"bbox": [10, 10, 50, 50], "score": 0.95},
            {"bbox": [60, 60, 100, 100], "score": 0.92},
            {"bbox": [110, 110, 150, 150], "score": 0.88},
            {"bbox": [160, 160, 200, 200], "score": 0.85},
            {"bbox": [210, 210, 250, 250], "score": 0.91},
            {"bbox": [260, 260, 300, 300], "score": 0.89}
        ]

def run_pipeline():
    print("--- Extracting Frames ---")
    extract_frames(video_path, "data/frames")

    print("\n--- Initializing AI Surveillance Architecture ---")
    model = DummyModel()
    model.eval()

    tracker = AdvancedTracker()
    event_detector = EventDetector(
        loiter_threshold=120,
        restricted_zones=[[(0, 0), (200, 0), (200, 200), (0, 200)]], # Example top-left corner
        crowd_threshold=5
    )
    
    # Initialize LangGraph Agentic Pipeline
    agent_graph = build_surveillance_graph()

    print("\n--- Running AI Pipeline ---")
    frame = cv2.imread("data/frames/frame_0.jpg")
    
    if frame is not None:
        # Detection
        detections = detect_people(model, frame)
        bounding_boxes = [d['bbox'] for d in detections]
        
        # Advanced Tracking
        tracked_objects = tracker.update(bounding_boxes)
        
        # Behavior/Event Detection
        events = event_detector.detect_events(tracked_objects, time.time())
        
        # Trigger Multi-Agent AI Workflows
        for evt in events:
            print(f"\n---> Firing Event Workflow: {evt['event']}")
            initial_state = {
                "event_name": evt["event"],
                "event_data": evt,
                "vision_context": "",
                "policy_context": "",
                "risk_level": "UNKNOWN",
                "report": "",
                "alert_triggered": False
            }
            # Execute workflow through nodes
            result_state = agent_graph.invoke(initial_state)
            print("--- Executed Graph Run ---")

if __name__ == "__main__":
    run_pipeline()
