from flask import Flask, Response, request, render_template, redirect
from datetime import datetime, date
import json
from flask_cors import CORS
# from marshmallow import Schema, post_load
# from marshmallow_enum import EnumField
# from flask_marshmallow import Marshmallow
import requests
from enum import Enum
import copy


# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)
# ma = Marshmallow(app)

EVENT_ENDPOINT = "http://54.91.230.210:5011"
ORGANIZER_ENDPOINT = "http://organizers-microservice-env.eba-3benqa5a.us-east-1.elasticbeanstalk.com"
ATTENDEE_ENDPOINT = "http://3.91.144.107:5021"


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Nimbus-Microservice",
        "health": "Good",
        "at time": t
    }

    result = Response(json.dumps(msg), status=200,
                      content_type="application/json")

    return result


@app.route("/organizer/<org_id>", methods=["GET"])
# Organizer Info + all events created
def organizer_info(org_id):
    """Returns organizer info and all events they have created
            Params: org_id the organizer's id
            Returns: dict[str:dict, str:dict]
    """
    organizer_info_rsp = requests.get(
        url=f"{ORGANIZER_ENDPOINT}/get_account_info/{org_id}")
    if organizer_info_rsp.status_code == 404:
        organizer_info = None
    else:
        organizer_info = organizer_info_rsp.json()

    event_data_rsp = requests.get(
        url=f"{EVENT_ENDPOINT}/event/organizer/{org_id}")
    if event_data_rsp.status_code == 404:
        event_data = None
    else:
        event_data = event_data_rsp.json()
    return dict(organizer_info=organizer_info, event_data=event_data)


@app.route("/attendee/<attendee_id>", methods=["GET"])
# Attendee Info + all events registered for
def attendee_info(attendee_id):
    """Returns attendee info and all events they have created
            Params: attendee_id the attendee's id
            Returns: dict[str:dict, str:dict]
    """
    attendee_info_rsp = requests.get(
        url=f"{ATTENDEE_ENDPOINT}/{attendee_id}")
    if attendee_info_rsp.status_code == 404:
        attendee_info = None
    else:
        attendee_info = attendee_info_rsp.json()

    event_data_rsp = requests.get(
        url=f"{EVENT_ENDPOINT}/event/attendee/{attendee_id}")
    if event_data_rsp.status_code == 404:
        event_data = None
    else:
        event_data = event_data_rsp.json()
    return dict(attendee_info=attendee_info, event_data=event_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
