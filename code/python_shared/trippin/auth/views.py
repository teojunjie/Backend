from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from python_shared.trippin.auth.permissions import (
    IsAuthenticatedWithServiceToken
)


class ServiceAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedWithServiceToken,)
