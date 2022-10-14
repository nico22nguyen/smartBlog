from json import dumps

from django.http import HttpResponse
from ..utils import getBody

def handler(request):
  pass

def getContacts(request, clientId):
  if request.method != 'GET':
    response = HttpResponse('Expected GET request')
    response.status_code = 405

    return response

  maxContacts = request.GET.get('max', None)

  # get maxContacts contacts from database
  # ------
  # ------

  resp_body = {
    'contacts': [ """ list of contacts """]
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def getContactById(request, clientId, contactId):
  if request.method != 'GET':
    response = HttpResponse('Expected GET request')
    response.status_code = 405

    return response

  # get contact by id from database
  # ------
  # ------

  resp_body = {
    'contact': ""# client from db 
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def createContact(request, clientId):
  if request.method != 'POST':
    response = HttpResponse('Expected POST request')
    response.status_code = 405

    return response

  body = getBody(request)
  contact = body['contact']

  # create contact in database
  # ------
  # ------

  resp_body = {
    'contact': contact
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def removeContact(request, clientId):
  if request.method != 'POST':
    response = HttpResponse('Expected POST request')
    response.status_code = 405

    return response

  body = getBody(request)
  contactId = body['contactId']

  # remove contact in database
  # ------
  # ------

  resp_body = {
    'contact': contactId
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')

def updateContact(request, clientIe):
  if request.method != 'POST':
    response = HttpResponse('Expected POST request')
    response.status_code = 405

    return response

  body = getBody(request)
  contactId = body['contactId']
  contactInfo = body['contact']

  # update contact in database
  # ------
  # ------

  resp_body = {
    'contact': contactId
  }

  return HttpResponse(dumps(resp_body), content_type='application/json')