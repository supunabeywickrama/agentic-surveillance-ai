def context_agent(event):
    rules = {
        "crowd_detected": "Crowd above 5 people may indicate risk"
    }

    return rules.get(event, "No rule found")
