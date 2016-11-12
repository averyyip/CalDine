from flask import Flask, Response, request
from twilio import twiml
from parser import addresses

app = Flask(__name__)


@app.route("/")
def check_app():
    # returns a simple string stating the app is working
    return Response("It works!"), 200


@app.route("/twilio", methods=["POST"])
def inbound_sms():
    response = twiml.Response()
    # we get the SMS message from the request. we could also get the
    # "To" and the "From" phone number as well
    inbound_message = request.form.get("Body")
    # we can now use the incoming message text in our Python application
    if inbound_message == "crossroads":
        response.message(addresses()['crossroads']['location'])
    else:
        response.message("Hi! Not quite sure what you meant, but okay.")
    # we return back the mimetype because Twilio needs an XML response
    return Response(str(response), mimetype="application/xml"), 200


i