import random
from numpy import dot
from numpy.linalg import norm
from django.shortcuts import redirect, render
from .models import RatingModel, WineModel, ReviewModel
import requests
from bs4 import BeautifulSoup
import re
from django.contrib.auth import get_user_model # 사용자가 데이터 베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import pandas as pd


tmp = pd.read_csv('C:\\Users\\Lee_DH\\Desktop\\running\\wine_data_for_recommendation.csv') # .drop('Unnamed: 0', axis=1)
df = pd.read_csv('C:\\Users\\Lee_DH\\Desktop\\running\\wine_data.csv')




# Create your views here.
def wine_crawling(target_wines):

    for target_wine in target_wines:

        name_split_list = target_wine.name.split(',')
        search_name = '+'.join(name_split_list)
        year = target_wine.year
        url = f'https://www.vivino.com/search/wines?q={search_name}+{year}'

        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
        wine = requests.get(url, headers=headers)
        soup = BeautifulSoup(wine.content, 'html.parser')

        try:
            wine_av = soup.select_one('.average__number').text
            wine_av = wine_av.strip('\n')
            if wine_av == '—':
                wine_av = str(0.0)
        except:
            wine_av = 0.0
        # target_wine.loc[i,'av_rating'] = wine_av

        try:
            target_element = soup.select_one('figure')['style']
        except:
            target_element = 0.0
        try:
            img_url = re.findall('\(([^)]+)', target_element)
            img_url = img_url[0].replace('//', '')
        except:
            img_url = 0.0

        # target_wine.loc[i,'img_url'] = img_url

        try:
            target_wine.av_rating = wine_av
            target_wine.img_url = img_url
        except:
            print('error')

        # print(i, "/", wine_av, " / ", img_url)
    
    return target_wines


def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))


def similarity(id):
    sim = []
    for i in range(0, len(tmp)):
        sim.append(cos_sim(tmp.iloc[id-1].values, tmp.iloc[i].values))

    coss = pd.DataFrame({'id' : df['id'][0:].tolist(), 'sim' : sim})

    sim_wines = pd.concat([df.reset_index().drop('index', axis=1), coss.drop('id', axis=1)], axis=1).sort_values(by=['sim'], ascending=False)[:10]
    
    return sim_wines


def home(request):
    wine_ids = WineModel.objects.all().values('id')

    wines = []
    for i in range(4):
        if len(wine_ids) > 0:
            random_id = random.choice(wine_ids)["id"]

            try:
                wine = WineModel.objects.get(pk=random_id)
                wines.append(wine)
            except wine.DoesNotExist:
                wine = None

    target_wine = wine_crawling(wines)

    # for i in range(0,4):
    #     print(target_wine[i].img_url)

    return render(request, 'main.html', {'wines': target_wine})





def wine_detail_view(request, id):
    wine = WineModel.objects.get(id=id)

    # 와인 정보 크롤링
    name_split_list = wine.name.split(',')
    search_name = '+'.join(name_split_list)
    year = wine.year

    url = f'https://www.vivino.com/search/wines?q={search_name}+{year}'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

    wine_info = requests.get(url, headers=headers)
    soup = BeautifulSoup(wine_info.content, 'html.parser')  
    target_element = soup.select_one('figure')['style']
    img_src = re.findall('\(([^)]+)', target_element)
    img_src = img_src[0].replace('//', '')

    if float(wine.av_rating) < 1.0 or wine.av_rating == '—':
        try:
            av_rating = soup.select_one('.average__number').text
            av_rating = av_rating.strip('\n')
        except:
            av_rating = '-'

        try:
            av_rating = av_rating.replace(',', '.')
            av_rating = float(av_rating)
        except:
            pass
    else:
        av_rating = float(wine.av_rating)

    # 리뷰
    reviews = ReviewModel.objects.filter(wine=wine).order_by('-created_at')

    # 추천 와인
    sim_wines = similarity(id)
    sim_wines_id = sim_wines['id'].tolist()
    
    target_wine2 = []
    for sim_wine in sim_wines_id:
        candidate_wine = WineModel.objects.get(product_id=sim_wine)
        target_wine2.append(candidate_wine)
    result = wine_crawling(target_wine2)

    result2 = sorted(result, key=lambda wine: wine.av_rating, reverse=True)[:4]

    # 기존 작성 리뷰 여부
    review_exist = ReviewModel.objects.filter(author=request.user, wine=wine)
    print(review_exist)
    if len(review_exist) == 0:
        exist = 0
    else:
        exist = 1
    print(exist)

    # wish 기능
    user = request.user
    click_wish = user.wine_wish.all()
    
    # if wine in click_wish:
    #     user.wine_wish.remove(wine)
    # else:
    #     user.wine_wish.add(wine)

    return render(request, 'detail.html', {'wine': wine, 'src': img_src, 'av_rating': av_rating, 'reviews': reviews, 'exist': exist, 'click_wish':click_wish})


@login_required
def create_review(request, id):
    author = request.user
    wine = WineModel.objects.get(id=id)
    content = request.POST.get('content')

    ## rating model 업데이트 먼저
    rating = request.POST.get('rating')
    
    rating_model = RatingModel(author=author, wine=wine, rating=rating)
    rating_model.save()

    rating_model = RatingModel.objects.get(author=author, wine=wine)
    review = ReviewModel(author=author, wine=wine, rating=rating_model, content=content)
    review.save()

    # wine정보에서 av_rating 변경
    rating_list = RatingModel.objects.filter(wine=wine)
    rating = 0
    for i in range(0, len(rating_list)):
        rating += rating_list[i].rating
    
    wine.av_rating = rating/len(rating_list)
    wine.save()

    return redirect('wines:wine_detail_view', id)


@login_required
def to_edit_review(request, review_id, wine_id):

    return render(request, 'edit_review.html', {'review_id': review_id, 'wine_id': wine_id})




@login_required
def edit_review(request, review_id, wine_id):
    review_model = ReviewModel.objects.get(id=review_id)
    author = request.user
    content = request.POST.get('content')
    rating = request.POST.get('rating')

    rating_model = RatingModel.objects.get(author=author, wine=review_model.wine)
    rating_model.rating = rating
    rating_model.save()

    review_model.content = content
    review_model.rating = rating_model
    review_model.save()

    # wine정보에서 av_rating 변경
    wine = WineModel.objects.get(id=wine_id)

    rating_list = RatingModel.objects.filter(wine=wine)
    rating = 0
    for i in range(0, len(rating_list)):
        rating += rating_list[i].rating
    
    wine.av_rating = rating/len(rating_list)
    wine.save()

    return redirect('wines:wine_detail_view', wine_id)


@login_required
def delete_review(request, review_id, wine_id):

    wine = WineModel.objects.get(id=wine_id)

    # review model 에서 삭제
    review_model = ReviewModel.objects.get(id=review_id)
    review_model.delete()

    # rating model 에서 삭제
    rating_model = RatingModel.objects.get(author=request.user, wine=wine)
    rating_model.delete()

    # wine정보에서 av_rating 변경
    rating_list = RatingModel.objects.filter(wine=wine)
    rating = 0
    if len(rating_list) == 0:
        wine.av_rating = 0
    else:
        for i in range(0, len(rating_list)):
            rating += rating_list[i].rating
        
        wine.av_rating = rating/len(rating_list)
    wine.save()

    return redirect('wines:wine_detail_view', wine_id)


def search(request):
        if request.method == 'POST':
            searched = request.POST['searched']        
            winename = WineModel.objects.filter(name__contains=searched)
            return render(request, 'search.html', {'searched': searched, 'winename': winename})
        else:
            return render(request, 'search.html', {})

















def add(request):
    print('start')
    df = pd.read_csv('C:\\Users\\Lee_DH\\Desktop\\\running\\wine_data.csv').drop('Unnamed: 0', axis=1)

    for i in range(0, 100):

        wine = WineModel()
        wine.name = df['name'][i]
        wine.producer = df['producer'][i]
        wine.nation = df['nation'][i]
        wine.local1 = df['local1'][i]
        wine.local2 = df['local2'][i]
        wine.local3 = df['local3'][i]
        wine.local4 = df['local4'][i]

        wine.varieties1 = df['varieties1'][i]
        wine.varieties2 = df['varieties2'][i]
        wine.varieties3 = df['varieties3'][i]
        wine.varieties4 = df['varieties4'][i]
        wine.varieties5 = df['varieties5'][i]
        wine.varieties6 = df['varieties6'][i]
        wine.varieties7 = df['varieties7'][i]
        wine.varieties8 = df['varieties8'][i]
        wine.varieties9 = df['varieties9'][i]
        wine.varieties10 = df['varieties10'][i]
        wine.varieties11 = df['varieties11'][i]

        wine.year = df['year'][i]
        wine.type = df['type'][i]
        wine.degree = 0
        wine.sweet = 0
        wine.acidity = 0
        wine.body = 0
        wine.tannin = 0
        wine.price = df['price'][i]
        wine.av_rating = 0
        
        wine.save()

    print('end')
    return render(request, 'detail.html')
