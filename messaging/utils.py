from twilio.rest import Client
import os

def send_sms(phone_number, message):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    client.messages.create(
        to=phone_number,
        from_='+255787717013',  # Replace with your Twilio phone number
        body=message
    )
