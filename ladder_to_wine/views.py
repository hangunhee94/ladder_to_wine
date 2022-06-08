from django.shortcuts import render, redirect


def home(request):
    return redirect('wines:wine_detail_view', 1)