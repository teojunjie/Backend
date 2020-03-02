from django.db import models

# Create your models here.
class FoodCard(models.Model):
  category = models.CharField(max_length=255, editable=False, null=True, blank=False)
  dollar_sign = models.IntegerField(null=True, blank=False)
  title = models.CharField(max_length=255, editable=False, null=True, blank=False)
  location = models.CharField(max_length=255, editable=False, null=True, blank=False)
  latitude = models.CharField(max_length=255, editable=False, null=True, blank=False)
  longitude = models.CharField(max_length=255, editable=False, null=True, blank=False)
  photo_reference = models.CharField(max_length=255, editable=False, null=True, blank=False)

class Review(models.Model):
  food_card = models.ForeignKey(
    FoodCard,
    related_name='reviews',
    on_delete=models.CASCADE
  )
  comment = models.CharField(max_length=255, editable=False, null=True, blank=False)
  username = models.CharField(max_length=255, editable=False, null=True, blank=False)
  rating = models.IntegerField(null=True, blank=False)

class Tag(models.Model):
  food_card = models.ForeignKey(
    FoodCard,
    related_name='tags',
    on_delete=models.CASCADE
  )
  title = models.CharField(
    max_length=255,
    editable=False,
    null=True,
    blank=False,
  )