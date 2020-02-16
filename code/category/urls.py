from django.conf.urls import url
from category.views import CategoryView


EXTERNAL_URL_PREFIX = 'v1'

urlpatterns = [
    url(r'^{url_prefix}/categories?$'.format(
        url_prefix=EXTERNAL_URL_PREFIX,
    ), CategoryView.as_view(), name='categories'),
]
