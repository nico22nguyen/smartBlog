from json import dumps

from django.http import HttpResponse
from ..utils import getBody, params_missing, connection

import uuid

def handler(request):
  if request.method == 'GET':
    # get user id query param (may or may not be provided)
    userId = request.GET.get('uid', None)

    # get user id specified else get all users
    return getUserById(userId) if userId else getUsers()

  if request.method == 'POST':
    user = None
    # get user obj from request body
    try:
      body = getBody(request)
      user = body['user']
    except:
      response = HttpResponse('Expected user in request body')
      response.status_code = 400

      return response
    return createUser(user)

  if request.method == 'DELETE':
    # get user id query param
    userId = request.GET.get('uid', None)
    if params_missing(userId):
      response = HttpResponse('Expected uid in query params')
      response.status_code = 400

      return response

    return deleteUser(userId)

  else:
    response = HttpResponse('This request type is unsupported: ' + request.method)
    response.status_code = 405

    return response


def getUsers():
  cursor = connection.cursor()

  cursor.execute('SELECT * FROM user')

  users = []
  for (iduser, email, password, first_name, last_name) in cursor:
    users.append({
      'first_name': first_name,
      'last_name': last_name,
      'email': email,
      'password': password,
      'iduser': iduser
    })

  cursor.close()
  return HttpResponse(dumps({ 'data': users }), content_type='application/json')

def getUserById(userId):
  cursor = connection.cursor()
  
  cursor.execute('SELECT * FROM user WHERE iduser = %s', [userId])
  result = cursor.fetchone()

  if cursor.rowcount == 0:
    response = HttpResponse('No user with id ' + userId)
    response.status_code = 404

    return response
  
  (iduser, email, password, first_name, last_name) = result

  user = {
    'first_name': first_name,
    'last_name': last_name,
    'email': email,
    'password': password,
    'iduser': iduser
  }

  cursor.close()
  return HttpResponse(dumps({ 'data': user }), content_type='application/json')

def createUser(user):
  cursor = connection.cursor()

  if params_missing([user['email'], user['password'], user['first_name'], user['last_name']]):
    response = HttpResponse('User object incomplete: expected email, password, first_name, and last_name')
    response.status_code = 400

    return response

  id = uuid.uuid4().hex
  query = f'INSERT INTO user (iduser, email, password, first_name, last_name) VALUES ("{id}", "{user["email"]}", "{user["password"]}", "{user["first_name"]}", "{user["last_name"]}")'
  cursor.execute(query)
  connection.commit()

  cursor.close()
  response = {
    'data': {'id': id }
  }

  return HttpResponse(dumps(response), content_type='application/json')

def deleteUser(userId):
  cursor = connection.cursor()

  cursor.execute('DELETE FROM user WHERE iduser = %s', [userId])
  if cursor.rowcount == 0:
    response = HttpResponse('No user with id ' + userId)
    response.status_code = 404

    return response
  connection.commit()

  cursor.close()
  resp_body = {
    'data': { 'id': userId }
  }
  
  return HttpResponse(dumps(resp_body), content_type='application/json')