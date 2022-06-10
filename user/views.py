from http.client import HTTP_PORT
import re
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
import requests
from .models import UserModel
from wine.models import WineModel, ReviewModel, RatingModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        nickname = request.POST.get('nickname', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if password != password2:
            return render(request, 'signup.html', {'error':'패스워드를 확인 해주세요.'})
        else:
            if username == '' or password == '':
                return render(request, 'signup.html', {'error': 'ID 와 비밀번호는 필수입니다.'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'signup.html', {'error': '이미 있는 ID입니다.'})
            else:
                UserModel.objects.create_user(username=username, nickname=nickname, password=password)
                return redirect('/sign-in')

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('wines:home')
        else:
            return render(request, 'signin.html', {'error':'ID 혹은 비밀번호를 확인 해주세요.'})

    elif request.method == 'GET':
        return render(request, 'signin.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/sign-in')

# 회원 정보 수정
def update_user(request):
    return

# 회원 정보 탈퇴
def delete_user(request):
    return 

# 회원 정보를 확인하고 회원이면, 회원 전용 페이지로 이동시키고,
# 그렇지 않으면 로그인 화면으로 이동
@login_required
def my_home(request):
    user = request.user.is_authenticated # 로그인이 되어 있는지 확인하는 기능
    if user:
        return render(request, 'user/my_home.html')
    else:
        return redirect('/')


# 찜 목록 가져오기
@login_required
def get_wish(request, id):
    user = UserModel.objects.get(id=id)
    if request.method == 'GET':
        wish_lists = user.wine_wish.all()
        # print(wish_lists)
        wine_list = []
        src_list = []
        for wish_list in wish_lists:
            # print(wish_list)
            wine_id = wish_list.id
            # print(wine_id)  # 숫자 키 값
            wine = WineModel.objects.get(id=wine_id)
            wine_list.append(wine)

            # src 주소 불러오기
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
            src_list.append(img_src)

        return render(request, 'user/my_wish.html', {'wine_list': wine_list, 'src_list':src_list})

# 찜 목록 추가하기
# id = wine_id, number
@login_required
def post_wish(request, id, code):
    wine = WineModel.objects.get(id=id)
    user = request.user
    click_wish = user.wine_wish.all()
    if wine in click_wish:
        user.wine_wish.remove(wine)
    else:
        user.wine_wish.add(wine)
    if code == 1:
        return redirect('wines:wine_detail_view', id)
    elif code == 2:
        return redirect('users:get_wish', user.id)
    # if number == 100:
    #     return redirect('wines:detail', user.id)
    # else:
    #     return redirect('users:post_wish', user.id)

# review 리스트 불러오기
@login_required
def get_review(request, id):
    user = UserModel.objects.get(id=id)
    review_list = ReviewModel.objects.filter(author_id=user).order_by('-created_at')

# 와인 정보 크롤링
    src_list = []
    for review in review_list:
        name_split_list = review.wine.name.split(',')
        search_name = '+'.join(name_split_list)
        year = review.wine.year

        url = f'https://www.vivino.com/search/wines?q={search_name}+{year}' 
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

        wine_info = requests.get(url, headers=headers)
        soup = BeautifulSoup(wine_info.content, 'html.parser')  
        target_element = soup.select_one('figure')['style']
        img_src = re.findall('\(([^)]+)', target_element)
        img_src = img_src[0].replace('//', '')
        src_list.append(img_src)
    print(src_list)

    return render(request, 'user/my_review.html', {'review_list': review_list, 'src_list': src_list})