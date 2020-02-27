from rest_framework.serializers import (
    ModelSerializer,
    CharField,
)

from category.models import (
    Category,
    CategoryType
)


class CategorySerializer(ModelSerializer):
    name = CharField()
    image_url = CharField()

    class Meta:
        model = Category
        fields = '__all__'


class CategoryTypeSerializer(ModelSerializer):
    name = CharField()
    image_url = CharField()

    class Meta:
        model = CategoryType
        fields = '__all__'
