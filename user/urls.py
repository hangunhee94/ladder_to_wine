from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('my/', views.my_home, name='my_home'),
    path('wish_list/<int:id>', views.get_wish, name='get_wish'),
    path('wishes/<int:id>/<int:code>', views.post_wish, name='post_wish'),
    path('review_list/<int:id>', views.get_review, name='get_review'),
]