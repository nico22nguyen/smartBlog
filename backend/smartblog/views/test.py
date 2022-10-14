from json import dumps

from django.http import HttpResponse
from ..utils import getBody

def test(request):
  if request.method == 'POST':
    body = getBody(request)
    testValue = body['testValue']

    resp_body = {
      'testValue * 2': testValue * 2
    }

    return HttpResponse(dumps(resp_body), content_type='application/json')
  elif request.method == 'GET':
    resp_body = {
      'testValue * 2': 69
    }

    return HttpResponse(dumps(resp_body), content_type='application/json')
  else:
    response = HttpResponse('Expected GET or POST request')
    response.status_code = 405

    return response