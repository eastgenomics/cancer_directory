from django.urls import path
from . import views
from .views import Nov20_View, Jul21_View


urlpatterns = [
    path(
        '',
        Jul21_View.as_view(),
        name='jul21_list',
        ),

    path(
        'Jul21_version/<str:test_code>/',
        views.jul21_detail,
        name='jul21_detail',
        ),

    path(
        'Nov20_version/', 
        Nov20_View.as_view(),
        name='nov20_list',
        ),
    
    path(
        'Nov20_version/<str:test_code>/',
        views.nov20_detail,
        name='nov20_detail',
        ),
]
