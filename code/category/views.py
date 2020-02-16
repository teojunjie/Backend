from django.shortcuts import render
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

from base_app import csrf

class CategoryView(APIView):
    
    authentication_classes = (csrf.CsrfExemptSessionAuthentication, csrf.BasicAuthentication)

    def post(self, request, *args, **kwargs):
        data = request.data
        
        name = data.get('name')
        image_url = data.get('image_url')
        
        updates = {
            'image_url': image_url
        }
        
        Category.objects.update_or_create(
            name=name,
            defaults=updates
        )
        
    def get(self, request, *args, **kwargs):
        categories = Categories.objects.prefetch_related('types').all()
        
        categories_data = []
        for category in categories:
            category_dict = {}
            cd = CategorySerializer(category)
            result = cd.data
            category_dict.update(**result)
            
            types = []
            for category_type in category.types.all():
                ct = CategoryTypeSerializer(category_type)
                types.append(ct.data)
            
            category_dict['types'] = types
            
            categories_data.append(category_dict)
        
        return Response(data=categories_data, status=status.HTTP_200_OK)
                
    def put(self, request, *args, **kwargs):
        data = request.data
        
        category_name = data.get('category_name')
        category_type_name = data.get('category_type_name')
        category_image_url = data.get('image_url')
        
        category, created = Category.objects.get_or_create(
            name=category_name,
            image_url=None,
        )

        updates = {
            'image_url': category_image_url,
            'category': category
        }        

        CategoryType.update_or_create(
            name=category_type_name,
            defaults=updates
        )
        
        return Response("Created category data successfully", status=status.HTTP_200_OK)
        
        

        
        
        
        