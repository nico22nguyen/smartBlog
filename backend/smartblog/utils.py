from os import getenv
from json import loads
from MySQLdb import connect
from dotenv import load_dotenv

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