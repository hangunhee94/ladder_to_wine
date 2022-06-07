from django.shortcuts import render
from .models import WineModel, ReviewModel
import requests
from bs4 import BeautifulSoup
import re


# Create your views here.
def selected_wine_detail_view(request, id):
    selected_wine = WineModel.objects.get(id=id)
    all_review = ReviewModel.objects.all().order_by('-created_at')
    name_split_list = selected_wine.name.split(',')
    search_name = '+'.join(name_split_list)
    year = selected_wine.year

    url = f'https://www.vivino.com/search/wines?q={search_name}+{year}' 
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

    wine = requests.get(url, headers=headers)
    soup = BeautifulSoup(wine.content, 'html.parser')  
    target_element = soup.select_one('figure')['style']
    item = re.findall('\(([^)]+)', target_element)
    img_src = item[0]




## review 작성
    author = request.user
    wine = WineModel.opjects.get(## name or pk)
    rating = request.POST.get('rating')
    content = request.POST.get('content')
    article = Article(title=title, content=content)
    article.save()





    return render(request, 'wine_detail.html', selected_wine, all_review, img_src)


