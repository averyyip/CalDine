from flask import Flask, Response, request
from twilio import twiml
from restaurant_parser import info, filtered_menu
import os

app = Flask(__name__)


@app.route("/")
def check_app():
    # returns a simple string stating the app is working
    return Response("Cal SMS App"), 200


@app.route("/twilio", methods=["POST"])
def inbound_sms():
    response = twiml.Response()
    # we get the SMS message from the request. we could also get the
    # "To" and the "From" phone number as well
    inbound_message = request.form.get("Body").lower().replace(' ', '')
    # we can now use the incoming message text in our Python application
    outbound_message = info()
    if 'info' in inbound_message:
        inbound_message = inbound_message.replace('info','')
    else:
        outbound_message.update(filtered_menu())
    if inbound_message in outbound_message.keys():
        response.message(inbound_message.upper() + '\n' + outbound_message[inbound_message] + '\n')
    else:
        commands = ''
        dc_commands = '\ncrossroads info \nfoothill info \ncafe3 info \nclarkkerr info'
        for key in outbound_message.keys():
            commands += '\n' + key
        response.message('Invalid command.\nTry :' + commands + dc_commands) #all the available options
    # we return back the mimetype because Twilio needs an XML response
    return Response(str(response), mimetype="application/xml"), 200


if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, port = int(port))