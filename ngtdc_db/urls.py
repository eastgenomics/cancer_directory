from django.urls import path
from . import views
from .views import TableListView


urlpatterns = [
    path('', TableListView.as_view()),
    path('tests/<str:test_code>/', views.test_detail, name='test_detail'),
]
