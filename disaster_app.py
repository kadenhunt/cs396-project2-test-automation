#the actual functions of the disaster response system

def parse_emergency_report(report):
    if "location" not in report or "severity" not in report:
        raise ValueError("Invalid report format")
    return {"location": report["location"], "severity": int(report["severity"])}

def assign_responder(report):
    responders = ["Alice", "Bob", "Charlie"]
    return responders[report["severity"] % len(responders)]

def update_resources(responder, status):
    resources = {"Alice": "available", "Bob": "available", "Charlie": "available"}
    resources[responder] = status
    return resources

def send_alert(message, location):
    return f"ALERT: {message} at {location}"