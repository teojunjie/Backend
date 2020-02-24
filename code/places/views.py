import json
from typing import (
    Dict,
    List,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from python_shared.trippin.util.decorators import validation_decorator
from places.places_util import (
    search_nearby_places,
    get_place_details,
)
from common.types import (
    PlaceBasicDict,
    PlaceDetailsDict
)


class RequestChoicesView(APIView):
    '''
    This view will be responsible for retrieving all places related to the
    user's request
    '''
    @validation_decorator
    def post(self, request, *args, **kwargs) -> Response:
        '''
        Body params:
        1) latitude
        2) longitude
        3) radius: the radius of the circle in which the search is made from
           the location
        4) type: the type of place to search for
        '''

        body: Dict = json.loads(request.body.decode('utf-8'))

        latitude: str = body.get('latitude')
        longitude: str = body.get('longitude')
        radius: str = body.get('radius')
        category_type: str = body.get('type')

        location: str = f'{latitude}, {longitude}'

        result: List[PlaceBasicDict] = search_nearby_places(
            location=location,
            radius=radius,
            category_type=category_type
        )

        if len(result) < 3:
            return Response(result, status.HTTP_200_OK)

        return Response(result[0:3], status.HTTP_200_OK)


class RequestChoicesDetailsView(APIView):
    '''
    This view will be reponsible for retrieving all details of the place
    '''

    @validation_decorator
    def post(self, request, *args, **kwargs) -> Response:
        '''
        kwargs:
        1) place_id: the id of the place used to make the search
        '''
        body: Dict = json.loads(request.body.decode('utf-8'))

        place_id: str = kwargs.get('place_id')
        fields: str = body.get('fields')

        result: PlaceDetailsDict = get_place_details(
            place_id=place_id,
            fields=fields
        )

        return Response(result, status.HTTP_200_OK)
