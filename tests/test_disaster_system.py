#simulating multiple reports and full end-to-end workflow 

import pytest
from disaster_app import parse_emergency_report, assign_responder, update_responder, send_alert

def test_system_workflow():
    #makeup reports and responders
    responders = {"Joe":"available", "Lamar":"available", "Josh":"available"}
    reports = [
        {"location": "NYC", "severity": 3},
        {"location": "LA", "severity": 1},
        {"location": "Chicago", "severity": 2}
    ]

    for report in reports:
        #parse the report at hand
        parsed = parse_emergency_report(report)
        assert "location" in parsed and "severity" in parsed

        #assign a responder to each report
        responder, responders = assign_responder(parsed, responders)
        assert responders[responder] == "busy"

        #send out an alert for the report
        alert = send_alert(f"Emergency reported", parsed["location"])
        assert parsed["location"] in alert

        #after one emergency is dealt with, make the responder available again
        responders = update_responder(responder, "available", responders)
        assert responders[responder] == "available"
    
    #make sure after all emergencies are dealt with responders are available again
    for status in responders.values():
        assert status == "available"