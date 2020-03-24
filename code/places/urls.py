from django.urls import (
    re_path,
)

from places.views import (
    RequestChoicesView,
    RequestChoicesDetailsView,
)

INTERNAL_URL_PREFIX = 'internal/v1/places'
EXTERNAL_URL_PREFIX = 'v1/places'

urlpatterns = [
    re_path(
        r'^{url_prefix}/choices/request?$'.format(
            url_prefix=EXTERNAL_URL_PREFIX,
        ),
        RequestChoicesView.as_view(),
        name='internal_request_choices'
    ),
    re_path(
        r'^{url_prefix}/choices/(?P<place_id>[^/]+)/details?$'.format(
            url_prefix=EXTERNAL_URL_PREFIX,
        ),
        RequestChoicesDetailsView.as_view(),
        name='internal_request_detail'
    )
]
