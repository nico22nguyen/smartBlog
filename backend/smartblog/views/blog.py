import uuid
from json import dumps

from django.http import HttpResponse
from ..utils import getBody, params_missing, connection

def handler(request):
  if request.method == 'GET':
    blog_id = request.GET.get('bid', None)
    user_id = request.GET.get('uid', None)
    title = request.GET.get('title', None)
    cgeq = request.GET.get('cgeq', None)
    cleq = request.GET.get('cleq', None)

    if (blog_id):
      return getBlogById(blog_id)
    elif (user_id or title or cleq or cgeq):
      if cgeq:
        cgeq=int(cgeq)
      if cleq:
        cleq=int(cleq)
      return getBlogsWithConstraints(user_id=user_id, title=title, cgeq=cgeq, cleq=cleq)
    else:
      return getAllBlogs()
  elif request.method == 'POST':
    blog = None
    # get user obj from request body
    try:
      body = getBody(request)
      blog = body['blog']
    except:
      response = HttpResponse('Expected blog in request body')
      response.status_code = 400

      return response
    return createBlog(blog)
  else:
    response = HttpResponse('This request type is unsupported: ' + request.method)
    response.status_code = 405

    return response

def getAllBlogs():
  cursor = connection.cursor()

  cursor.execute('SELECT * FROM blog')
  result = cursor.fetchall()
  blogs = getBlogsFromQueryResult(result)

  cursor.close()
  return HttpResponse(dumps({ 'data': blogs }), content_type='application/json')

def getBlogById(blog_id):
  cursor = connection.cursor()

  cursor.execute('SELECT * FROM blog WHERE idblog = %s', [blog_id])

  result = cursor.fetchone()

  if cursor.rowcount == 0:
    response = HttpResponse('No blog with id ' + blog_id)
    response.status_code = 404

    return response
  
  (idblog, user_id, title, content, created_at, rating) = result

  blog = {
    'idblog': idblog,
    'user_id': user_id,
    'title': title,
    'content': content,
    'created_at': str(created_at),
    'rating': rating
  }

  cursor.close()
  return HttpResponse(dumps({ 'data': blog }), content_type='application/json')

def getBlogsWithConstraints(user_id, title, cgeq, cleq):
  # make sure constraints are valid
  if (not params_missing([cleq, cgeq]) and cgeq > cleq):
    response = HttpResponse('cgeq must be less than or equal to cleq')
    response.status_code = 400

    return response
  
  # count constraints (for query building)
  numConstraints = 0
  for constraint in [user_id, title, cgeq, cleq]:
    if constraint:
      numConstraints += 1
  
  # quick helper for repeated code
  def add_AND_if_needed():
    nonlocal numConstraints
    nonlocal query
    numConstraints -= 1
    if numConstraints > 0:
      query += ' AND'

  # build query from params, add ANDs where necessary
  query = 'SELECT * FROM blog WHERE'
  if user_id:
    query += f' user_id = "{user_id}"'
    add_AND_if_needed()
  if title:
    query += f' title = "{title}"'
    add_AND_if_needed()
  if cgeq:
    query += f' rating >= {cgeq}'
    add_AND_if_needed()
  if cleq:
    query += f' rating <= {cleq}'

  print(query)
  cursor = connection.cursor()
  cursor.execute(query)
  result = cursor.fetchall()
  blogs = getBlogsFromQueryResult(result)

  cursor.close()
  return HttpResponse(dumps({ 'data': blogs }), content_type='application/json')

# handle error for no such user, myql will throw one
def createBlog(blog):
  cursor = connection.cursor()

  if params_missing([blog['user_id'], blog['title'], blog['content'], blog['created_at'], blog['rating']]):
    response = HttpResponse('User object incomplete: expected email, password, first_name, and last_name')
    response.status_code = 400

    return response

  id = uuid.uuid4().hex
  query = f'INSERT INTO blog (idblog, user_id, title, content, created_at, rating) VALUES ("{id}", "{blog["user_id"]}", "{blog["title"]}", "{blog["content"]}", "{blog["created_at"]}", "{blog["rating"]}")'

  # need to handle email already taken
  cursor.execute(query)
  connection.commit()

  cursor.close()
  response = {
    'data': {'id': id }
  }

  return HttpResponse(dumps(response), content_type='application/json')

# helper function to get blogs from query result
def getBlogsFromQueryResult(result):
  blogs = []
  for (idblog, user_id, title, content, created_at, rating) in result:
    blogs.append({
    'idblog': idblog,
    'user_id': user_id,
    'title': title,
    'content': content,
    'created_at': str(created_at),
    'rating': rating
  })

  return blogs