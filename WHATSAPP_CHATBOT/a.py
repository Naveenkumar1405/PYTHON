from fastapi import FastAPI, Request, HTTPException
from twilio.rest import Client
import keys
from threading import Timer
from twilio.base.exceptions import TwilioRestException
import logging
logging.basicConfig(filename='bot_errors.log', level=logging.ERROR)
app = FastAPI()

account_sid = keys.account_sid
auth_token = keys.auth_token
client = Client(account_sid, auth_token)

sessions, authlist = {}, {}

def send_whatsapp_message(to, body, media_url=None):
    try:
        message = client.messages.create(
            body=body,
            from_='whatsapp:+917708630275',  # Your Twilio number
            to='whatsapp:' + to,
            media_url=media_url
        )
        return {'status': 'Message sent', 'sid': message.sid}  # The ID of the message
    except TwilioRestException as e:
        raise HTTPException(status_code=400, detail=f"Error sending message: {e}")


def send_whatsapp_message(to, body):
    message = client.messages.create(
        body=body,
        from_='whatsapp:+917708630275',  # Your Twilio number
        to='whatsapp:' + to
    )
    return {'status': 'Message sent', 'sid': message.sid}  # The ID of the message


@app.post("/webhook")
async def read_item(request: Request):
    form_data = await request.form()
    ProfileName = form_data.get('ProfileName')
    Body = form_data.get('Body')
    From = form_data.get('From')  # Get the user's phone number

    user_message = Body.lower()

    def session_timeout(From):
        try:
            del authlist[From]
            send_whatsapp_message(to = From, body = "Your *session* has *timeout* due to inactive on the channel. Please type *'Hi'* to go to the welcome message")
        except:
            send_whatsapp_message(to = From, body = "Oops invalid format, Please type *'Hi'* to go to the welcome message")
    timer = Timer(900, session_timeout,[From])
    timer.start()
    sessions[From] = timer


    if From in sessions:
        timer = sessions[From]
        timer.cancel()

    if user_message == "hi":
        message = f"Hi {ProfileName}! Welcome to ONWORDS. I am ONYX , The Personalised assistant for ONWORDS. Let me know something about you,can you lend me a click."
        if From not in authlist:
            authlist[From] = From
        return send_whatsapp_message(From, message)

    else:
      if From in authlist:
        if user_message == "t":
            return send_whatsapp_message(From, "yes its working")

        elif user_message in ["3", "option 3"]:
            # Process Option 3
            message = 'You chose Option 3. [Continue your response here]'
            return send_whatsapp_message(From, message)

        else:
            message = 'Invalid message. Please type "Hi" to start or select one of the given options.'
            return send_whatsapp_message(From, message)
