from django.urls import path

from . import views
from .views import (
    Nov20MainList,
    Nov20CIList,
    Jul21MainList,
    Jul21CIList,
    )


urlpatterns = [
    path(
        '',
        Jul21MainList.as_view(),
        name='jul21_main_list',
        ),
    
    path(
        'Jul21_CI_List/',
        Jul21CIList.as_view(),
        name='jul21_ci_list',
        ),

    path(
        'Jul21_Test_Detail/<str:test_code>/',
        views.jul21_test_detail,
        name='jul21_test_detail',
        ),

    path(
        'Jul21_CI_Detail/<str:ci_code>/',
        views.jul21_ci_detail,
        name='jul21_ci_detail',
        ),


    path(
        'Nov20_Main_List/', 
        Nov20MainList.as_view(),
        name='nov20_main_list',
        ),

    path(
        'Nov20_CI_List/',
        Nov20CIList.as_view(),
        name='nov20_ci_list',
        ),

    path(
        'Nov20_Test_Detail/<str:test_code>/',
        views.nov20_test_detail,
        name='nov20_test_detail',
        ),

    path(
        'Nov20_CI_Detail/<str:ci_code>/',
        views.nov20_ci_detail,
        name='nov20_ci_detail',
        ),
]
