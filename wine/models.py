from django.db import models
from user.models import UserModel
from django.conf import settings


# Create your models here.
class WineModel(models.Model):
    class Meta:
        db_table = "wines"

    index = models.IntegerField(default='')
    product_id = models.CharField(max_length=256, default='')
    name = models.CharField(max_length=256, default='')
    producer = models.CharField(max_length=256, default='')
    nation = models.CharField(max_length=256, default='')
    local1 = models.CharField(max_length=256, default='')
    local2 = models.CharField(max_length=256, default='')
    local3 = models.CharField(max_length=256, default='')
    local4 = models.CharField(max_length=256, default='')

    varieties1 = models.CharField(max_length=256, default='')
    varieties2 = models.CharField(max_length=256, default='')
    varieties3 = models.CharField(max_length=256, default='')
    varieties4 = models.CharField(max_length=256, default='')
    varieties5 = models.CharField(max_length=256, default='')
    varieties6 = models.CharField(max_length=256, default='')
    varieties7 = models.CharField(max_length=256, default='')
    varieties8 = models.CharField(max_length=256, default='')
    varieties9 = models.CharField(max_length=256, default='')
    varieties10 = models.CharField(max_length=256, default='')
    varieties11 = models.CharField(max_length=256, default='')
    varieties12 = models.CharField(max_length=256, default='')

    type = models.CharField(max_length=256, default='')
    use = models.CharField(max_length=256, default='')
    abv = models.FloatField(max_length=256, default='')
    degree = models.FloatField(max_length=256, default='')
    sweet = models.IntegerField(default='')
    acidity = models.IntegerField(default='')
    body = models.IntegerField(default='')
    tannin = models.IntegerField(default='')
    price = models.IntegerField(default='')
    year = models.IntegerField(default='')
    ml = models.IntegerField(default='')
    av_rating = models.FloatField(max_length=256, default='')
    img_url = models.CharField(max_length=256, default='')

    wish = models.ManyToManyField(UserModel)


class RatingModel(models.Model):
    class Meta:
        db_table = "ratings"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    wine = models.ForeignKey(WineModel, on_delete=models.CASCADE)
    rating = models.FloatField(max_length=256, default='')


class ReviewModel(models.Model):
    class Meta:
        db_table = "reviews"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    wine = models.ForeignKey(WineModel, on_delete=models.CASCADE)
    rating = models.ForeignKey(RatingModel, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
