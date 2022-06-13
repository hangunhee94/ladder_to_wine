from django.contrib import admin
from .models import RatingModel, WineModel, ReviewModel

# Register your models here.
admin.site.register(RatingModel)
admin.site.register(WineModel)
admin.site.register(ReviewModel)