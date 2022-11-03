from json import dumps

from django.http import HttpResponse
from ..utils import getBody, params_missing

def handler(request):
  if request.method != 'POST':
    response = HttpResponse('Must POST to login route')
    response.status_code = 405

    return response

  body = getBody(request)
  content = body['content']

  # ensure email and password are provided
  if params_missing([content]):
    response = HttpResponse('Expected content in request body')
    response.status_code = 400

    return response
  
  twitter_analysis = analyze_twitter(content)
  instagram_analysis = analyze_instagram(content)
  average = (twitter_analysis + instagram_analysis) / 2

  response = {
    'data': {
      'twitter_analysis': twitter_analysis,
      'instagram_analysis': instagram_analysis,
      'average_analysis': average
    }
  }

  return HttpResponse(dumps(response), content_type='application/json')

def analyze_twitter(body):
  return 50

def analyze_instagram(body):
  return 75