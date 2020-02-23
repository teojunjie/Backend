from django.db import models
from places.constants import PRICE_LEVEL_CHOICES


class PlaceDetails(models.Model):
    phone_number = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        help_text="The local phone number associated with the place"
    )
    price_level = models.IntegerField(
        blank=True,
        null=True,
        choices=PRICE_LEVEL_CHOICES,
        help_text="The price level of the place"
    )
    rating = models.FloatField(
        blank=True,
        null=True,
        help_text="The aggregated rating of the place"
    )
    category_icon_url = models.TextField(
        blank=True,
        null=True,
        help_text="The icon url of the category related to this place"
    )
    google_maps_url = models.TextField(
        blank=True,
        null=True,
        help_text="The google maps url of the place"
    )
    website = models.TextField(
        blank=True,
        null=True,
        help_text="The website associated with the place"
    )


class Place(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        help_text="The name of the place"
    )
    address = models.TextField(
        unique=True,
        blank=False,
        null=True,
        help_text="The address associated with the place"
    )
    place_id = models.CharField(
        unique=True,
        blank=False,
        null=True,
        max_length=255,
        help_text=(
            "The id associated with the place, "
            "this has to be unique"
        )
    )
    details = models.OneToOneField(
        PlaceDetails,
        on_delete=models.CASCADE,
        related_name='details',
        null=True
    )


class PlacePhotos(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='photos',
        null=True
    )
    photo_reference = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        help_text="The reference id associated with this photo"
    )
    height = models.IntegerField(
        blank=False,
        null=True,
        help_text="The height associated with the image returned"
    )
    width = models.IntegerField(
        blank=False,
        null=True,
        help_text="The width associated with the image returned"
    )


class PlaceReviews(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )
    author_name = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        help_text="The name of the author associated with this review"
    )
    rating = models.IntegerField(
        blank=False,
        null=True,
        help_text="The rating given by the author for the place"
    )
    text = models.TextField(
        blank=True,
        null=True,
        help_text="The user's review with respect to the place"
    )
    profile_photo_url = models.TextField(
        blank=True,
        null=True,
        help_text="The user's profile image url"
    )
