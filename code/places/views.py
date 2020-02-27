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
    PlaceDetailsDict,
    PlaceFullDict,
    PlaceDataDict,
    PlaceReviewDict,
    PlaceTagDict,
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
        category: str = body.get('category')
        keyword: str = body.get('keyword')

        location: str = f'{latitude}, {longitude}'

        places: List[PlaceBasicDict] = search_nearby_places(
            location=location,
            radius=radius,
            category_type=category_type,
            keyword=keyword
        )

        data: List[PlaceFullDict] = []
        for place in places:
            place_id: str = place.get('place_id')
            place_details: PlaceDetailsDict = get_place_details(
                place_id=place_id
            )
            place_tags: List[PlaceTagDict] = place_details.get('tags')
            place_reviews: List[PlaceReviewDict] = place_details.get('reviews')
            place_data_dict: PlaceDataDict = {
                'category': category,
                'dollar_sign': place_details.get('dollar_sign'),
                'title': place.get('name'),
                'location': place.get('address'),
                'latitude': place_details.get('latitude'),
                'longitude': place_details.get('longitude'),
                'aggregated_rating': place_details.get('aggregated_rating'),
                "photo_reference_id": place.get('photo_reference_id')
            }
            place_full_dict: PlaceFullDict = {
                'data': place_data_dict,
                'reviews': place_reviews,
                'tags': place_tags
            }
            data.append(place_full_dict)

        if len(data) < 3:
            return Response(data, status.HTTP_200_OK)

        return Response(data[0:3], status.HTTP_200_OK)


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

        if fields:
            result: PlaceDetailsDict = get_place_details(
                place_id=place_id,
                fields=fields
            )

            return Response(result, status.HTTP_200_OK)

        result: PlaceDetailsDict = get_place_details(
            place_id=place_id,
        )

        return Response(result, status.HTTP_200_OK)
