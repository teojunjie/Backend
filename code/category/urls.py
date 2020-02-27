from django.urls import (
    re_path
)
from category.views import (
    CategoryAddView,
    CategoryListView,
    CategoryTypeAddView,
    CategoryTypeListView,
    CategoryBatchAddView
)


EXTERNAL_URL_PREFIX = 'v1'

urlpatterns = [
    re_path(
        r'^{url_prefix}/categories/list?$'.format(
            url_prefix=EXTERNAL_URL_PREFIX,
        ),
        CategoryListView.as_view(),
        name='categories_list'
    ),
    re_path(
        r'^{url_prefix}/categories/batch/add?$'.format(
            url_prefix=EXTERNAL_URL_PREFIX,
        ),
        CategoryBatchAddView.as_view(),
        name='categories_batch_add'
    ),
    re_path(
        r'^{url_prefix}/categories/(?P<name>[^/]+)/add?$'.format(
            url_prefix=EXTERNAL_URL_PREFIX,
        ),
        CategoryAddView.as_view(),
        name='categories_add'
    ),
    re_path(
        r'^{url_prefix}/category/type/(?P<name>[^/]+)/add?$'.format(
            url_prefix=EXTERNAL_URL_PREFIX,
        ),
        CategoryTypeAddView.as_view(),
        name='category_type_add'
    ),
    re_path(
        r'^{url_prefix}/category/type/(?P<name>[^/]+)/list?$'.format(
            url_prefix=EXTERNAL_URL_PREFIX,
        ),
        CategoryTypeListView.as_view(),
        name='category_type_list'
    ),
]
