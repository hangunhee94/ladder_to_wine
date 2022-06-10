from django.urls import path
from . import views

app_name = 'wines'
urlpatterns = [
    path('', views.home, name='home'),
    path('wine/<int:id>', views.wine_detail_view, name='wine_detail_view'),
    path('review/create/<int:id>', views.create_review, name='create_review'),
    path('review/to-edit/<int:review_id>/<int:wine_id>/<int:code>', views.to_edit_review, name='to_edit_review'),
    path('review/edit/<int:review_id>/<int:wine_id>/<int:code>', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/<int:wine_id>/<int:code>', views.delete_review, name='delete_review'),
    path('search/', views.search, name='search'),
]


    