from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_get_from_instagram, name='index'),
    path('details/<int:instagram_user_id>', views.get_details, name='details'),
]
