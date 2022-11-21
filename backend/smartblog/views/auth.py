from django.http import HttpResponse
from json import dumps
from ..utils import getBody, params_missing, connection, getHashedString

def handler(request):
  if request.method != 'POST':
    response = HttpResponse('Must POST to login route')
    response.status_code = 405

    return response

  body = getBody(request)
  email = body['email']
  raw_password = body['password']

  # ensure email and password are provided
  if params_missing([email, raw_password]):
    response = HttpResponse('Expected email and password in request body')
    response.status_code = 400

    return response

  # prevent sql injections
  if ';' in email:
    response = HttpResponse('Invalid email')
    response.status_code = 400

    return response

  cursor = connection.cursor()
  cursor.execute(f'SELECT iduser, password FROM user WHERE email = "{email}"')
  (id, correct_hash) = cursor.fetchone()

  # 404 if no user with provided email
  if cursor.rowcount == 0:
    response = HttpResponse('No user with email ' + email)
    response.status_code = 404

    return response
  
  attempt_hash = getHashedString(raw_password)

  if attempt_hash == correct_hash:
    return HttpResponse(dumps({ 'data': {'userId': id } }), content_type='application/json')
  else:
    response = HttpResponse('Incorrect Password')
    response.status_code = 401
    return response