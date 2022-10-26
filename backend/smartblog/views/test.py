from json import dumps

from django.http import HttpResponse
from ..utils import getBody, connection

cursor = connection.cursor()

def test(request):
  if request.method == 'POST':
    body = getBody(request)
    testValue = body['testValue']

    resp_body = {
      'testValue * 2': testValue * 2
    }

    return HttpResponse(dumps(resp_body), content_type='application/json')
  elif request.method == 'GET':
    cursor.execute('SELECT * FROM user')

    users = []
    for (iduser, email, password, first_name, last_name) in cursor:
      print({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'iduser': iduser
      })
      users.append({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'iduser': iduser
      })
    resp_body = {
      'testValue * 2': 69,
      'users': users
    }

    return HttpResponse(dumps(resp_body), content_type='application/json')
  else:
    response = HttpResponse('Expected GET or POST request')
    response.status_code = 405

    return response