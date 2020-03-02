from django.conf.urls import url
from .views import (
  Signin, 
  Signup,
)

EXTERNAL_URL_PREFIX = 'v1'

urlpatterns = [
    url(r'^{url_prefix}/signin?$'.format(
        url_prefix=EXTERNAL_URL_PREFIX,
    ), Signin.as_view(), name='signin'),

    url(r'^{url_prefix}/signup?$'.format(
        url_prefix=EXTERNAL_URL_PREFIX,
    ), Signup.as_view(), name='signup'),
]
