import requests
import urllib.parse
import tweepy

from json import dumps, loads
from dotenv import load_dotenv
from os import getenv
from django.http import HttpResponse

from ..utils import getBody, params_missing, remove_escape_chars

load_dotenv()

NUM_KEYWORDS = 5
NUM_TWEETS_PER_SEARCH = 10
KEYWORDS_URL = 'https://textanalysis-keyword-extraction-v1.p.rapidapi.com/keyword-extractor-text'
SENTIMENT_URL = 'https://japerk-text-processing.p.rapidapi.com/sentiment/'

tweepy_client = tweepy.Client(
  getenv('TWITTER_BEARER_TOKEN'),
  getenv('TWITTER_CONSUMER_KEY'),
  getenv('TWITTER_CONSUMER_SECRET'),
  getenv('TWITTER_ACCESS_TOKEN'),
  getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

def handler(request):
  if request.method != 'POST':
    response = HttpResponse('Must POST to login route')
    response.status_code = 405

    return response

  body = getBody(request)
  text = body['text']

  # ensure email and password are provided
  if params_missing([text]):
    response = HttpResponse('Expected text in request body')
    response.status_code = 400

    return response

  keywords = get_keywords(text)
  print(keywords)
  tweets = []
  for keyword in keywords:
    tweets += get_tweets_by_keyword(keyword)
  print(tweets)
  twitter_analyses = [get_text_analysis(tweet) for tweet in tweets]
  print(twitter_analyses)

  twitter_score = get_controversy_from_analyses(twitter_analyses)
  response = {
    'data': {
      'twitter_analysis': twitter_score,
      'instagram_analysis': 'Not implemented',
      'average_analysis': 'Not implemented',
    }
  }
  return HttpResponse(dumps(response), content_type='application/json')

def get_keywords(text):
  data = f'wordnum={NUM_KEYWORDS}&text={urllib.parse.quote(text)}'
  headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'X-RapidAPI-Key': '5d168941fcmshfd5fec745122b99p1ed8fajsn4ac2b5781ca7',
    'X-RapidAPI-Host': 'textanalysis-keyword-extraction-v1.p.rapidapi.com'
  }

  api_response = requests.request('POST', KEYWORDS_URL, data=data, headers=headers)

  keywords = loads(api_response.text)['keywords']
  return keywords

def get_tweets_by_keyword(keyword):
  response_body = tweepy_client.search_recent_tweets(
    query=f'{keyword} -is:retweet',
    sort_order='relevancy',
    tweet_fields='text',
    max_results=NUM_TWEETS_PER_SEARCH
  )

  if not response_body.data:
    return []
  return [remove_escape_chars(tweet.text) for tweet in response_body.data]

def get_text_analysis(text):
  data = f'text={urllib.parse.quote(text)}'
  headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'X-RapidAPI-Key': '5d168941fcmshfd5fec745122b99p1ed8fajsn4ac2b5781ca7',
    'X-RapidAPI-Host': 'japerk-text-processing.p.rapidapi.com'
  }

  response_raw = requests.request('POST', SENTIMENT_URL, data=data, headers=headers)
  probability_obj = loads(response_raw.text)['probability']
  return probability_obj

def get_controversy_from_analyses(analyses):
  CONTROVERSY_WEIGHT = 0.67
  ANTI_NEUTRALITY_WEIGHT = 0.33
  sums = { 'neg': 0, 'neutral': 0, 'pos': 0 }

  for score in analyses:
    sums['neg'] += score['neg']
    sums['neutral'] += score['neutral']
    sums['pos'] += score['pos']
    
  print(sums)

  # get controversy from number of positive vs negative tweets (the closer the sums, the more controversial the subject)
  controversy = 1 - (sums['pos'] - sums['neg']) / len(analyses)

  # get how NOT neutral the tweets are on average
  anti_neutrality = 1 - (sums['neutral'] / len(analyses))

  controversy_score = (controversy * CONTROVERSY_WEIGHT + anti_neutrality * ANTI_NEUTRALITY_WEIGHT) / 1

  print(f'raw controversy: {controversy}')
  print(f'anti_neutrality: {anti_neutrality}')
  print(f'final controversy: {controversy_score}')

  return controversy_score

def analyze_instagram(body):
  return 75