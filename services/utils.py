from twilio.rest import Client

def send_sms(to_phone_number, verification_code):
    account_sid = 'ACcfe1a58d15e7ae923967ca5474a22f23'
    auth_token = '73fb6a75433ccadb93141270609ff2f8'
    from_phone_number = '+12172150851'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your verification code is: {verification_code}",
        from_=from_phone_number,
        to=to_phone_number
    )
