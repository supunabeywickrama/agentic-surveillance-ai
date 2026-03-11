def alert_agent(event, risk):
    alert = f"ALERT: {event} | Risk Level: {risk}"
    print(alert)
    return alert
