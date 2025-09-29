#simulating multiple reports and full end-to-end workflow 

import pytest
from disaster_app import parse_emergency_report, assign_responder, update_responder, send_alert

def test_system_workflow():
    #makeup reports and responders
    responders = {
        "Joe":"available", 
        "Lamar":"available",
        "Josh": "available"
    }

    reports = [
        {"location": "NYC", "severity": 3},
        {"location": "LA", "severity": 1},
        {"location": "Chicago", "severity": 2}
    ]
    
    assigned = {}
    alerts = []

    for report in reports:
        try:
            #parse the report at hand
            parsed = parse_emergency_report(report)
            assert "location" in parsed and "severity" in parsed

            #assign a responder to each report
            responder, responders = assign_responder(parsed, responders)
            assert responders[responder] == "busy"

            #send out an alert for the report
            alerts.append(send_alert(f"Emergency reported", parsed["location"]))

            assigned[parsed["location"]]=responder
        except: 
            assigned[report.get("location", "UNKNOWN")] = None

    assert len(assigned) == len(reports) #checks if all emergencies are processed
    assert all("ALERT:" in msg for msg in alerts) #checks that alerts were sent for all valid reports
    
    #after all disasters are handled, set responders back to available
    for responder in responders.keys():
        responders = update_responder(responder, "available", responders)
    
    #make sure after all emergencies are dealt with responders are available again
    assert all(status == "available" for status in responders.values())
