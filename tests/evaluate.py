import json

def evaluate_predictions(ground_truth, predictions):
    """
    Computes precision, recall, and detection accuracy for events.
    
    Args:
        ground_truth: list of dicts, e.g. [{"event": "loitering", "person_id": 1}]
        predictions: list of dicts, e.g. [{"event": "loitering", "person_id": 1}]
    """
    print("--- 📊 Evaluation Metrics ---")
    
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    
    gt_pairs = {(gt["event"], gt.get("person_id", -1)) for gt in ground_truth}
    pred_pairs = {(pred["event"], pred.get("person_id", -1)) for pred in predictions}
    
    for pred in pred_pairs:
        if pred in gt_pairs:
            true_positives += 1
        else:
            false_positives += 1
            
    for gt in gt_pairs:
        if gt not in pred_pairs:
             false_negatives += 1
             
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Generic accuracy over detected frames
    print(f"✅ Detection Precision:    {precision*100:.1f}%")
    print(f"🎯 Event Detection Recall: {recall*100:.1f}%")
    print(f"📈 F1-Score:               {f1_score*100:.1f}%")
    print(f"🚨 False Positive Rate:    {false_positives} false alarms generated")
    print(f"⚠️ False Negatives:        {false_negatives} missed events")

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score
    }

if __name__ == "__main__":
    print("Running sample evaluation...")
    sample_gt = [
        {"event": "loitering", "person_id": 1},
        {"event": "crowd_detected", "person_id": -1},
        {"event": "restricted_area_entry", "person_id": 2}
    ]
    
    sample_preds = [
        {"event": "loitering", "person_id": 1},
        {"event": "crowd_detected", "person_id": -1},
        {"event": "loitering", "person_id": 3} # False positive
    ]
    
    metrics = evaluate_predictions(sample_gt, sample_preds)
