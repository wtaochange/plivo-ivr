#from flask import Flask
#application = Flask(__name__)

#@application.route("/")
#def hello():
#    return "Hello World!"

#if __name__ == "__main__":
#    application.run()

from flask import Flask, Response, request, url_for
import plivoxml

# This file will be played when a caller presses 2.
PLIVO_SONG = "https://s3.amazonaws.com/plivocloud/music.mp3"

# This is the message that Plivo reads when the caller dials in
IVR_MESSAGE1 = "Welcome to the Plivo IVR Demo App. Press 1 to listen to a pre recorded text in different languages.  \
                Press 2 to listen to a song."

IVR_MESSAGE2 = "Press 1 for English. Press 2 for French. Press 3 for Russian"
# This is the message that Plivo reads when the caller does nothing at all
NO_INPUT_MESSAGE = "Sorry, I didn't catch that. Please hangup and try again \
                    later."

# This is the message that Plivo reads when the caller inputs a wrong number.
WRONG_INPUT_MESSAGE = "Sorry, it's wrong input."

app = Flask(__name__)

@app.route('/response/ivr/', methods=['GET','POST'])
def ivr():
    response = plivoxml.Response()
    if request.method == 'GET':
        getdigits_action_url = url_for('ivr', _external=True)
        getDigits = plivoxml.GetDigits(action=getdigits_action_url,
        method='POST', timeout=7, numDigits=1,
        retries=1)

        getDigits.addSpeak(IVR_MESSAGE1)
        response.add(getDigits)
        response.addSpeak(NO_INPUT_MESSAGE)
        print response.to_xml()
        return Response(str(response), mimetype='text/xml')

    elif request.method == 'POST':
        digit = request.form.get('Digits')
        print digit
        if digit == "1":
            # Read out a text.
            getdigits_action_url1 = url_for('tree', _external=True)
            getDigits1 = plivoxml.GetDigits(action=getdigits_action_url1,
            method='POST', timeout=7, numDigits=1,
            retries=1)
            getDigits1.addSpeak(IVR_MESSAGE2)
            response.add(getDigits1)
            response.addSpeak(NO_INPUT_MESSAGE)

        elif digit == "2":
            # Listen to a song
            response.addPlay(PLIVO_SONG)

        else:
            response.addSpeak(WRONG_INPUT_MESSAGE)

        print response.to_xml()
        return Response(str(response), mimetype='text/xml')

@app.route('/response/tree/', methods=['GET','POST'])
def tree():
    response = plivoxml.Response()
    digit = request.form.get('Digits')

    if digit == "1":
        text = u"This message is being read out in English"
        params = {
            'language': "en-GB",
        }
        response.addSpeak(text,**params)

    elif digit == "2":
        text = u"Ce message est lu en français"
        params = {
            'language': "fr-FR",
        }
        response.addSpeak(text,**params)

    elif digit == "3":
        text = u"Это сообщение было прочитано в России"
        params = {
            'language': "ru-RU",
        }
        response.addSpeak(text,**params)

    else:
        response.addSpeak(WRONG_INPUT_MESSAGE)

    print response.to_xml()
    return Response(str(response), mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
