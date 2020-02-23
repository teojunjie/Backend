import logging
from typing import (
    List,
    Dict
)

from common.types import (
    PlaceBasicDict,
    PlaceDetailsDict,
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
) -> List[Dict[str, PlaceBasicDict]]:
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
                f'key={api_token}'
            )
        )
        results: List[Dict[str, PlaceBasicDict]] = body.get('results')
        return results

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
    fields: str,
) -> PlaceDetailsDict:

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
        result = body.get('result')
        return result

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
