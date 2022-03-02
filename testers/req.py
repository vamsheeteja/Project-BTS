
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = 'ACf30a1fed8d98a3f1576de13e511db950'
# auth_token = '2c3914ae241f4d9af34f5f7aaeb40089'
# client = Client(account_sid, auth_token)

# mob = "+917993152245"

# message = client.messages \
#     .create(
#          body='hii',
#          from_='+12672043203',
#          to=mob
#      )

# print("hiii")
# print(message.sid)

phone_number = "7993152245"
account_sid = "AC979102757cfbe11a2724d91d3348bc87"
auth_token = "448bc767d695ed87a66b38dd6474d257"
client = Client(account_sid, auth_token)
verification_check = client.verify.services("VAb4329cd9592b157108db040fb9601cf9").verification_checks.create(to="+917993152245", code= '1234')

print(verification_check.status)

# verify = client.verify.services('MG3f3fb649a397cd6a7cb1a94667e8c6dd')
# verify.verifications.create(to="+91"+phone_number, channel='sms')



# verify = client.verify.services('VA3f98da905f54dc5f728300d7321f6ef4')
# verify.verifications.create(to=mob, channel='sms')

# n = int(input('enter code: '))
# result = verify.verification_checks.create(to=mob, code=n)
# print(result.status)


# validation_request = client.validation_requests.create(
#                                 friendly_name='My Home Phone Number',
#                                 phone_number=mob
#                             )
# print(validation_request.validation_code)
'''
outgoing_caller_ids = client.outgoing_caller_ids.list(phone_number=mob)
print(outgoing_caller_ids)
'''
