import cv2

def detect_people(model, frame):
    results = model(frame)
    detections = []

    for result in results:
        bbox = result['bbox']
        confidence = result['score']

        detections.append({
            "bbox": bbox,
            "confidence": confidence
        })

    return detections
