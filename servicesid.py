from twilio.rest import Client


account_sid = 'AC979102757cfbe11a2724d91d3348bc87'
auth_token = '448bc767d695ed87a66b38dd6474d257'
client = Client(account_sid, auth_token)

service = client.messaging.services.create(friendly_name='friendly_name')

print(service.sid)