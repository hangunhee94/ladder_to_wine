from django.shortcuts import render, redirect

from wine.models import WineModel


def home(request):
    return redirect('wines:wine_detail_view', 1)

    