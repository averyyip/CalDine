from flask import Flask, Response, request
from twilio import twiml
from restaurant_parser import info, filtered_menu
import os

app = Flask(__name__)

def filter_input(message):
    comparison = [['calcentral', 'calcentrl', 'clcentral'], 
    ['qualcomm', 'qualcom', 'qulcomm'],
    ['crossroads', 'crossroad', 'crosroads', 'xroads', 'croads', 'croad'],
    ['cafe3', 'cafe three', 'cfe3', 'café3', 'caféthree'],
    ['foothill', 'fothill', 'foothil'],
    ['clarkkerr', 'ck', 'clarkerr', 'ckc', 'clarkkerrcampus'],
    ['bearwalk', 'berwalk', 'burrwalk', 'oskiwalk'],
    ['gbc', 'goldenbearcafe', 'goldenbear'],
    ['ucpd', 'ucpolice', 'police']
    ]

    if 'info' in message:
        message = inbound_message.replace('info','')

    for service in comparison:
        if message in service:
            return service[0]

help_message = 'Text Options:\n Text "restaurant name"(without the quotes) for the menu(if available).\nText "<restaurant name> info"(without the quotes) for information about the service or location.' 

@app.route("/")
def check_app():
    # returns a simple string stating the app is working
    return Response("Cal SMS App"), 200


@app.route("/twilio", methods=["POST"])
def inbound_sms():
    response = twiml.Response()
    # we get the SMS message from the request. we could also get the
    # "To" and the "From" phone number as well
    inbound_message = filter_input(request.form.get("Body").lower().replace(' ', ''))
    # we can now use the incoming message text in our Python application
    outbound_message = info()
    if 'help' in inbound_message:
        response.message(help_message)
    else:
        outbound_message.update(filtered_menu())
    if inbound_message in outbound_message.keys():
        response.message(inbound_message.upper() + '\n' + outbound_message[inbound_message] + '\n')
    else:
        commands = ''
        dc_commands = '\ncrossroads info \nfoothill info \ncafe3 info \nclarkkerr info'
        for key in outbound_message.keys():
            commands += '\n' + key
        response.message("Sorry, I don't recognize that location. Reply with one of our commands below for more information.<\n" + commands.title() + dc_commands + '\nText "helpme" for help') #all the available options
    # we return back the mimetype because Twilio needs an XML response
    return Response(str(response), mimetype="application/xml"), 200


if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host = '0.0.0.0', port = int(port))

