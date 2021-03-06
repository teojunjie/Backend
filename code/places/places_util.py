import logging
from typing import (
    List,
    Dict,
    Union,
    Any,
)

from common.types import (
    PlaceBasicDict,
    PlaceDetailsDict,
    PlaceReviewDict,
    PlaceTagDict
)
from common.exceptions import PlacesException
from places.places_client import PlacesClient

logger = logging.getLogger('places_util')


def get_places_client() -> PlacesClient:
    '''
    Returns an initialized PlacesClient with api key loaded
    into params
    '''
    return PlacesClient()


def get_place_from_text(
    input_text: str,
    input_type: str,
    fields: str,
    location_bias: str,
) -> List[Dict[str, PlaceBasicDict]]:
    '''
    A Find Place request takes a text input and returns a place.
    The input can be any kind of Places text data, such as a name, address,
    or phone number. The request must be a string. A Find Place request using
    non-string data such as a lat/lng coordinate or plus code generates an
    error.
    '''

    client: PlacesClient = get_places_client()
    api_token: str = client._get_api_token()

    try:
        response, body = client.get(
            relative_uri=(
                'findplacefromtext/json?'
                f'input={input_text}&'
                f'inputtype={input_type}&'
                f'fields={fields}&'
                f'key={api_token}'
            )
        )
        candidates: List[Dict[str, PlaceBasicDict]] = body.get('candidates')
        return candidates

    except Exception as e:
        logger.warning(
            'Unknown exception occurred while getting place data'
            'Exceptions is %s',
            e
        )
        raise PlacesException(
            'Unknown exception occurred while getting place data'
            'Exceptions is %s',
            e
        )


def search_nearby_places(
    location: str,
    radius: int,
    category_type: str,
    keyword: str,
) -> List[PlaceBasicDict]:
    '''
    A Nearby Search lets you search for places within a specified area.
    You can refine your search request by supplying keywords or specifying the
    type of place you are searching for.
    '''

    client: PlacesClient = get_places_client()
    api_token: str = client._get_api_token()

    try:
        response, body = client.get(
            relative_uri=(
                'nearbysearch/json?'
                f'location={location}&'
                f'radius={radius}&'
                f'type={category_type}&'
                f'keyword={keyword}&'
                f'key={api_token}'
            )
        )
        results: List[Dict[str, Any]] = body.get('results')
        places: List[PlaceBasicDict] = []
        for result in results:
            place_dict: Dict[str, str] = {
                'name': result.get('name'),
                'address': result.get('vicinity'),
                'place_id': result.get('place_id'),
            }

            photos: Dict[str, Union[str, int]] = result.get('photos')
            if photos:
                place_dict['photo_reference_id'] = (
                    photos[0].get('photo_reference')
                )

            places.append(place_dict)

        return places

    except Exception as e:
        logger.warning(
            'Unknown exception occurred while getting nearby place data'
            'Exceptions is %s',
            e
        )
        raise PlacesException(
            'Unknown exception occurred while getting nearby place data'
            'Exceptions is %s',
            e
        )


def get_place_details(
    place_id: str,
    fields: str = 'rating,geometry,price_level,review,type',
) -> PlaceDetailsDict:
    '''
    A Place Details request returns more comprehensive information about the
    indicated place such as its complete address, phone number,
    user rating and reviews.
    '''

    logger.info(
        f'Getting details for place {place_id}'
    )

    client: PlacesClient = get_places_client()
    api_token: str = client._get_api_token()

    try:
        response, body = client.get(
            relative_uri=(
                'details/json?'
                f'place_id={place_id}&'
                f'fields={fields}&'
                f'key={api_token}'
            )
        )
        result: Dict[str, Any] = body.get('result')
        place_details_dict: PlaceDetailsDict = {
            "dollar_sign": result.get('price_level'),
            "aggregated_rating": result.get('rating'),
            'latitude': result['geometry']['location']['lat'],
            'longitude': result['geometry']['location']['lng']
        }

        # Grab the reviews if any
        reviews: List[Dict[str, str]] = result.get('reviews')
        reviews_data: List[PlaceReviewDict] = []
        review_dict: PlaceReviewDict = None

        if reviews:
            for review in reviews:
                review_dict = {
                    'comment': review.get('text'),
                    'author_name': review.get('author_name'),
                    'rating': review.get('rating')
                }
                reviews_data.append(review_dict)

        # Grab the tags if any
        tags: List[PlaceTagDict] = result.get('types')
        tags_data: List[PlaceTagDict] = []
        tag_dict: PlaceTagDict = None

        if tags:
            for tag in tags:
                tag_dict = {
                    'title': tag
                }
                tags_data.append(tag_dict)

        place_details_dict['reviews'] = reviews_data
        place_details_dict['tags'] = tags_data

        return place_details_dict

    except Exception as e:
        logger.warning(
            'Unknown exception occurred while getting nearby place data'
            'Exceptions is %s',
            e
        )
        raise PlacesException(
            'Unknown exception occurred while getting nearby place data'
            'Exceptions is %s',
            e
        )
