from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from foodcard.models import (
  FoodCard, 
  Review, 
  Tag
)
from foodcard.serializers import (
  FoodCardSerializer,
  TagSerializer,
  ReviewSerializer
)

import random as rand
import json
from base_app import csrf

import requests
apikey = 'AIzaSyC8e6d1V5puPyhxd3G-JEQ-HB2NVtNXCt8'
geoencoding_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}'
places_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'

# Create your views here.
class FoodCardView(APIView):
  authentication_classes = (csrf.CsrfExemptSessionAuthentication, csrf.BasicAuthentication)

  def post(self, request, *args, **kwargs):
    data = request.data.get('data')

    for jsonObj in data:
      geocode = jsonObj.get('geoCode')
      lat, lng = geocode.get('latitude'), geocode.get('longitude')
      title = jsonObj.get('name')
      category = jsonObj.get('category')
      tags = jsonObj.get('tags')

      full_geoencoding_url = geoencoding_url.format(str(lat), str(lng), apikey)
      
      location_content = requests.get(full_geoencoding_url)
      location_res = json.loads(location_content.text).get('results')
      location_match = ""

      review_objects = []
      if len(location_res) >= 1:
        location_match = location_res[0].get('formatted_address')
        place_id = location_res[0].get('place_id')
        full_places_url = places_url.format(place_id, apikey)
        places_content = requests.get(full_places_url)
        places_res = json.loads(places_content.text)

        result_res = places_res.get('result')
        reviews = result_res.get('reviews')
        photos = result_res.get('photos')

        if reviews == None or photos == None:
          print('No reviews or photos found')
          continue

        photo_ref = photos[0].get('photo_reference')

        card = FoodCard.objects.create(
          category=category, 
          dollar_sign=rand.randint(1, 3), 
          title=title, 
          location=location_match,
          latitude=lat,
          longitude=lng,
          photo_reference=photo_ref
        )

        r_cnt = 0
        for rev in reviews:
          if r_cnt >= 5:
            break
          r = Review.objects.create(
            food_card=card,
            comment=rev.get('text')[:254], 
            username=rev.get('author_name'), 
            rating=rev.get('rating'),
          )
          r.save()
          r_cnt += 1
          review_objects.append(r)


      for review in review_objects:
        card.reviews.add(review)
        card.save()

      for tag_title in tags:
        t = Tag.objects.create(
          food_card=card,
          title=tag_title
        )
        t.save()

    return Response(status=status.HTTP_201_CREATED)


  def get(self, request, *args, **kwargs):
    food_cards = (
      FoodCard.objects
      .prefetch_related('tags', 'reviews')
      .all()
    )

    cards = []
    for card in food_cards:
      tags = card.tags.all()
      reviews = card.reviews.all()

      tags_data = []
      for tag in tags:
        t = TagSerializer(tag)
        tags_data.append(t.data)
      
      reviews_data = []
      for review in reviews:
        r = ReviewSerializer(review)
        reviews_data.append(r.data)

      c = FoodCardSerializer(card)
      cards.append(
        dict(
          data=c.data,
          reviews=reviews_data,
          tags=tags_data
        )
      )
    return Response(data=cards, status=status.HTTP_200_OK)
