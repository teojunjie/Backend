from typing import (
    NewType,
    List,
    Tuple,
)
from mypy_extensions import TypedDict

DjangoChoices = NewType('DjangoChoices', List[Tuple[str, str]])


class PlaceBasicDict(TypedDict):
    '''
    Returns the fields of a basic place
    '''
    name: str
    address: str
    place_id: str


class PlaceDetailsDict(TypedDict):
    '''
    Returns the details fields of the place
    '''
    phone_number: str
    price_level: str
    rating: float
    category_icon_url: str
    google_maps_url: str
    website: str
