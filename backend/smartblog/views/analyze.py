from json import dumps

from django.http import HttpResponse
from ..utils import getBody

def handler(request):
  pass

def getLogs(request):
  if request.method != 'GET':
    response = HttpResponse('Expected GET request')
    response.status_code = 405

    return response

  maxLogs = request.GET.get('max', None)

  # get maxLogs logs from database
  # ------
  # ------

  resp_body = {
    'logs': [ """ list of logs """]
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def getClientLogs(request, clientId):
  if request.method != 'GET':
    response = HttpResponse('Expected GET request')
    response.status_code = 405

    return response

  maxLogs = request.GET.get('max', None)

  # get maxLogs logs from database
  # ------
  # ------

  resp_body = {
    'logs': [ """ list of logs """]
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def getContactLogs(request, clientId, contactId):
  if request.method != 'GET':
    response = HttpResponse('Expected GET request')
    response.status_code = 405

    return response

  maxLogs = request.GET.get('max', None)

  # get maxLogs logs from database
  # ------
  # ------

  resp_body = {
    'logs': [ """ list of logs """]
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def getInventoryLogs(request, clientId, inventoryId):
  if request.method != 'GET':
    response = HttpResponse('Expected GET request')
    response.status_code = 405

    return response

  maxLogs = request.GET.get('max', None)

  # get maxLogs logs from database
  # ------
  # ------

  resp_body = {
    'logs': [ """ list of logs """]
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def getResourceLogs(request, clientId, inventoryId, resourceId):
  if request.method != 'GET':
    response = HttpResponse('Expected GET request')
    response.status_code = 405

    return response

  maxLogs = request.GET.get('max', None)
  
  print(clientId, inventoryId, resourceId)

  # get maxLogs logs from database
  # ------
  # ------

  resp_body = {
    'logs': [ """ list of logs """]
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')