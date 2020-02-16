from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    IntegerField,
    DateTimeField,
    FloatField,
    BooleanField,
)

from foodcard.models import FoodCard, Tag, Review

class FoodCardSerializer(ModelSerializer):
  category = CharField()
  dollar_sign = IntegerField()
  title = CharField()
  location = CharField()
  latitude = CharField()
  longitude = CharField()
  photo_reference = CharField()

  class Meta:
    model = FoodCard
    fields = '__all__'

class TagSerializer(ModelSerializer):
  title = CharField()

  class Meta:
    model = Tag
    fields = '__all__'


class ReviewSerializer(ModelSerializer):
  comment = CharField()
  username = CharField()
  rating = IntegerField()

  class Meta:
    model = Tag
    fields = '__all__'