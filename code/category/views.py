import json
import logging
from typing import (
    Dict,
    List,
)

from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from category.models import (
    Category,
    CategoryType,
)
from category.serializers import (
    CategorySerializer,
    CategoryTypeSerializer
)


logger = logging.getLogger('category_views')


class CategoryAddView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        Adds a category with its corresponding image

        Body params:
        1) name: name of category
        2) image_url: the link to the image for the category
        '''
        body: Dict = json.loads(request.body.decode('utf-8'))

        name = kwargs.get('name')
        image_url = body.get('image_url')

        updates = {
            'image_url': image_url
        }

        category, _ = Category.objects.update_or_create(
            name=name,
            defaults=updates
        )

        return Response(
            data=CategorySerializer(category).data,
            status=status.HTTP_200_OK
        )


class CategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        List all out all categories
        '''
        categories: QuerySet[Category] = Category.objects.all()

        results: List[Dict[str, str]] = []

        for category in categories:
            cd: CategorySerializer = CategorySerializer(category)
            category_data: Dict[str, str] = cd.data
            results.append(category_data)

        return Response(data=results, status=status.HTTP_200_OK)


class CategoryTypeAddView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        Adds a category type to the category

        Body params:
        1) category_name
        2) category_type_name
        3) image_url
        '''

        body: Dict = json.loads(request.body.decode('utf-8'))

        category_name: str = kwargs.get('name')
        category_type_name: str = body.get('category_type_name')
        category_image_url: str = body.get('image_url')

        try:
            category: Category = Category.objects.get(
                name=category_name,
            )
        except ObjectDoesNotExist:
            logger.info(
                f'Category {category_name} does not exist... Please create '
                'category first'
            )
            return Response(
                f'Category {category_name} does not exist... '
                'Please create category first',
                status.HTTP_404_NOT_FOUND
            )

        updates: Dict[str, str] = {
            'image_url': category_image_url,
            'category': category
        }

        CategoryType.objects.update_or_create(
            name=category_type_name,
            defaults=updates
        )

        return Response(
            "Created category data successfully",
            status=status.HTTP_200_OK
        )


class CategoryTypeListView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        List out all category types for that category

        kwargs:
        1) name: the name of the category
        '''

        category_name: str = kwargs.get('name')

        category_types: QuerySet[CategoryType] = (
            CategoryType.objects
            .filter(category__name=category_name)
            .all()
        )

        results: List[Dict[str, str]] = []

        for category_type in category_types:
            ct: CategoryTypeSerializer = CategoryTypeSerializer(category_type)
            ct_data: Dict[str, str] = ct.data
            results.append(ct_data)

        return Response(results, status.HTTP_200_OK)
