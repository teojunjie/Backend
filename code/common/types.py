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
    photo_reference_id: str


class PlaceReviewDict(TypedDict):
    '''
    Returns a review fields for the place
    '''
    comment: str
    author_name: str
    rating: str


class PlaceTagDict(TypedDict):
    title: str


class PlaceDetailsDict(TypedDict):
    '''
    Returns the details fields of the place
    '''
    dollar_sign: str
    aggregated_rating: float
    latitude: str
    longitude: str
    reviews: List[PlaceReviewDict]
    tags: List[PlaceTagDict]


class PlaceDataDict(TypedDict):
    category: str
    dollar_sign: str
    title: str
    location: str
    latitude: str
    longitude: str
    aggregated_rating: str


class PlaceFullDict(TypedDict):
    data: PlaceDataDict
    reviews: List[PlaceReviewDict]
    tags: List[PlaceTagDict]
    