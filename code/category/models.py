from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        editable=False,
        null=True,
        blank=False,
        unique=True,
    )
    image_url = models.CharField(
        max_length=255,
        editable=False,
        null=True,
        blank=False,
    )
    

class CategoryType(models.Model):
    name = models.CharField(
        max_length=255,
        editable=False,
        null=True,
        blank=False,
        unique=True,
    )
    image_url = models.CharField(
        max_length=255,
        editable=False,
        null=True,
        blank=False,
    )
    category = models.ForeignKey(
        Category,
        related_name='types',
        on_delete=models.CASCADE
    )