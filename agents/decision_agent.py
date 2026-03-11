def decision_agent(event):
    if event == "crowd_detected":
        return "MEDIUM RISK"
    return "LOW RISK"
