from django.urls import path
from .views import *

urlpatterns = [
    path('api/auth', auth.handler),
    path('api/user', user.handler),
    path('api/blog', blog.handler),
    path('api/analyze', analyze.handler),
]