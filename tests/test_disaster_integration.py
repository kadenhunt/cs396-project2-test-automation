#simulating a singular full disaster response workflow to ensure parts work together

import pytest
from disaster_app import parse_emergency_report, assign_responder, update_responder, send_alert

def test_disaster_integration():
    responders = {"Joe":"available", "Lamar":"available", "Josh":"available"}
    report = {"location": "NYC", "severity": 3}

    #parse the incoming report so the data is correctly formatted
    report = parse_emergency_report(report)
    assert "location" in report and "severity" in report

    #assign a responder to the scene
    responder, responders = assign_responder(report, responders)
    assert responders[responder] == "busy"

    #send out an alert
    alert = send_alert("Fire reported", report["location"])
    assert report["location"] in alert

    #after the emergency is dealt with, make the responder available again
    responders = update_responder(responder, "available", responders)
    assert responders[responder] == "available"