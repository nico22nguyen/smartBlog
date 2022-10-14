from hashlib import sha256
from django.http import HttpResponse
from ..utils import getBody

def handler(request):
  if request.method != 'POST':
    response = HttpResponse('Must POST to login route')
    response.status_code = 405

    return response

  body = getBody(request)
  email = body['email']
  raw_password = body['password']

  hashed_password = getHashedString(raw_password)


  # Send cross check given password with password from database
  # ------
  # ------

  correct_password = 'PASS FROM DB'

  if correct_password == hashed_password:
    return HttpResponse('Login Successful')
  else:
    response = HttpResponse('Incorrect Password')
    response.status_code = 403
    return response

# takes in string and returns sha256 hash of string
def getHashedString(input):
  # create hash object and feed it the input string
  hash_object = sha256()
  buffer = input.encode('utf-8')
  hash_object.update(buffer)

  # read the hash state
  return hash_object.hexdigest()