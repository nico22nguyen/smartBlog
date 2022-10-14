from json import dumps

from django.http import HttpResponse
from ..utils import getBody

def handler(request):
  pass

def getInventories(request, clientId):
  if request.method != 'GET':
    response = HttpResponse('Expected GET request')
    response.status_code = 405

    return response

  maxInventories = request.GET.get('max', None)

  # get maxInventories inventories from database
  # ------
  # ------

  resp_body = {
    'inventories': [ """ list of inventories """]
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def getInventoryById(request, clientId, inventoryId):
  if request.method != 'GET':
    response = HttpResponse('Expected GET request')
    response.status_code = 405

    return response

  # get inventory by id from database
  # ------
  # ------

  resp_body = {
    'inventory': ""# inventory from db 
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def createInventory(request, clientId):
  if request.method != 'POST':
    response = HttpResponse('Expected POST request')
    response.status_code = 405

    return response

  body = getBody(request)
  inventory = body['inventory']

  # create inventory in database
  # ------
  # ------

  resp_body = {
    'inventory': inventory
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def removeInventory(request, clientId):
  if request.method != 'POST':
    response = HttpResponse('Expected POST request')
    response.status_code = 405

    return response

  body = getBody(request)
  inventoryId = body['inventoryId']

  # remove inventory in database
  # ------
  # ------

  resp_body = {
    'inventory': inventoryId
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def updateInventory(request, clientId):
  if request.method != 'POST':
    response = HttpResponse('Expected POST request')
    response.status_code = 405

    return response

  body = getBody(request)
  inventoryId = body['inventoryId']
  inventoryInfo = body['inventory']

  # update inventory in database
  # ------
  # ------

  resp_body = {
    'inventory': inventoryId
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')