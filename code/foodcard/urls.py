from django.conf.urls import url
from foodcard.views import FoodCardView 


EXTERNAL_URL_PREFIX = 'v1'

urlpatterns = [
    url(r'^{url_prefix}/foodcard?$'.format(
        url_prefix=EXTERNAL_URL_PREFIX,
    ), FoodCardView.as_view(), name='foodcard'),
]
