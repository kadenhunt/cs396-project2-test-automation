#the functions of the disaster response system
import random
import logging

logging.basicConfig(level=logging.INFO)

#processes a incoming emergency report
def parse_emergency_report(report):
    if "location" not in report or "severity" not in report:
        #send an error if the report is missing info
        raise ValueError("Invalid report format") 
    
    #returns a report ensuring severity is an int
    return {"location": report["location"], "severity": int(report["severity"])}


#assigns a responder (if available) to an emergency
def assign_responder(report, responders):
    #find all the available responders
    available = [name for name, status in responders.items() if status == "available"]

    #if none are available send an error
    if not available:
        raise RuntimeError("No responders available")

    #pick one at random
    chosen = random.choice(available)
    responders[chosen] = "busy" #mark the responder as busy
    logging.info(f"Responder {chosen} assigned to {report['location']}")
    return chosen, responders

#updates the status of a responder
def update_responder(responder, status, responders):
    #send an error if the responder isnt in the dicttionary
    if responder not in responders:
        raise ValueError(f"Responder {responder} not found")
    
    #update and return
    responders[responder] = status
    logging.info(f"Responder update: {responder} is now {status}")
    return responders

#sends an alert message out
def send_alert(message, location):
    alertMessage = f"ALERT: {message} at {location}"
    logging.info(alertMessage)
    return alertMessage