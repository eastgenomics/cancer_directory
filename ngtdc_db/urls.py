from django.urls import path

from . import views
from .views import (
    V1MainList,
    V2MainList,
    V1CIList,
    V2CIList,
    )


urlpatterns = [
    path(
        'v1/', 
        V1MainList.as_view(),
        name='v1_main_display',
        ),

    path(
        '',
        V2MainList.as_view(),
        name='v2_main_display',
        ),

    path(
        'v1/ci/',
        V1CIList.as_view(),
        name='v1_ci_display',
        ),

    path(
        'v2/ci/',
        V2CIList.as_view(),
        name='v2_ci_display',
        ),

    path(
        'v1/test/<str:test_id>/',
        views.v1_test_detail,
        name='v1_test_detail',
        ),

    path(
        'v2/test/<str:test_id>/',
        views.v2_test_detail,
        name='v2_test_detail',
        ),

    path(
        'v1/ci/<str:ci_code>/',
        views.v1_ci_detail,
        name='v1_ci_detail',
        ),

    path(
        'v2/ci/<str:ci_code>/',
        views.v2_ci_detail,
        name='v2_ci_detail',
        ),
]
