from os import getenv
from json import loads
from MySQLdb import connect
from dotenv import load_dotenv
from hashlib import sha256

# nic was here!!!
load_dotenv()
connection = connect("localhost", getenv('DB_USER'), getenv('DB_PASS'), getenv('DB_NAME'))

# extracts the body of a post request
def getBody(request):
  body_unicode = request.body.decode('utf-8')
  return loads(body_unicode)

def callProcSafe(procName, args=None):
  cursor = connection.cursor()
  if args:
    res = cursor.callproc(procName, args)
  else:
    res = cursor.callproc(procName)
  cursor.close()

  return res

# helper function for checking if all required fields are present
def params_missing(params):
  for param in params:
    if not param:
      return True
  return False

# takes in string and returns sha256 hash of string
def getHashedString(input):
  # create hash object and feed it the input string
  hash_object = sha256()
  buffer = input.encode('utf-8')
  hash_object.update(buffer)

  # read the hash state
  return hash_object.hexdigest()

def remove_escape_chars(string: str):
  return string.replace('\n', ' ').replace('\r', ' ').replace('\xa0', ' ')