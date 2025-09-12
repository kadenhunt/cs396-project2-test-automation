#the actual testing script

import pytest
from disaster_app import parse_emergency_report, assign_responder, update_resources, send_alert

def test_parse_valid_report():
    report = {"location": "NYC", "severity": 3}
    parsed = parse_emergency_report(report)
    assert parsed["location"] == "NYC"
    assert parsed["severity"] == 3

def test_parse_invalid_report():
    with pytest.raises(ValueError):
        parse_emergency_report({"location": "NYC"})

def test_assign_responder():
    report = {"location": "LA", "severity": 2}
    responder = assign_responder(report)
    assert responder in ["Alice", "Bob", "Charlie"]

def test_update_resources():
    updated = update_resources("Alice", "busy")
    assert updated["Alice"] == "busy"

def test_send_alert():
    result = send_alert("Fire reported", "NYC")
    assert "Fire reported" in result
    assert "NYC" in result