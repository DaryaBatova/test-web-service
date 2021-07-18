from django.urls import path
from . import views

urlpatterns = [
    path('page/<int:pk>/', views.page_detail, name='get_page_detail'),
    path('page/', views.page_create, name='create_page_detail'),
]
