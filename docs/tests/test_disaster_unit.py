#unit testing script for the disaster response app

import pytest
from disaster_app import parse_emergency_report, assign_responder, update_responder, send_alert

#check that the report is parsed correctly
def test_parse_report_pass():
    report = {"location": "NYC", "severity": 3}
    parsed = parse_emergency_report(report)
    assert parsed["location"] == "NYC"
    assert parsed["severity"] == 3

#check that missing fields raise an error
def test_parse_report_fail():
    with pytest.raises(ValueError):
        parse_emergency_report({"location": "NYC"})

#check that an available responder gets assigned
def test_assign_responder_pass():
    report = {"location": "LA", "severity": 2}
    responders = {"Joe":"available", "Lamar":"available", "Josh":"available"}
    responder, updated = assign_responder(report, responders)
    assert responder in updated
    assert updated[responder]== "busy"

#check that assigning fails if all responders are busy
def test_assign_responder_fail():
    report = {"location": "LA", "severity": 2}
    responders = {"Joe":"busy", "Lamar":"busy", "Josh":"busy"}
    with pytest.raises(RuntimeError):
        assign_responder(report, responders)

#check if responder status is successfully updated
def test_update_responder_pass():
    responders = {"Joe":"available", "Lamar":"available", "Josh":"available"}
    updated = update_responder("Joe", "busy", responders)
    assert updated["Joe"] == "busy"

#checking if update responder sends an error when it fails
def test_update_responder_fail():
    responders = {"Joe":"available", "Lamar":"available", "Josh":"available"}
    with pytest.raises(ValueError):
        update_responder("Patrick", "busy", responders)

#check that alerts include both message and location
def test_send_alert():
    msg = send_alert("Fire reported", "NYC")
    assert "Fire reported" in msg
    assert "NYC" in msg