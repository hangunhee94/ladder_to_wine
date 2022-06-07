from django.urls import path
from . import views

app_name = 'wines'
urlpatterns = [
    path('<int:id>', views.wine_detail_view),
]


    