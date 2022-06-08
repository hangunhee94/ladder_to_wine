from http.client import HTTP_PORT
from django.shortcuts import render, redirect
from .models import UserModel
from wine.models import WineModel
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
            return HttpResponse(me.nickname + "님 환영합니다.")
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
    if request.method == 'GET':
        user = UserModel.objects.get(id=id)
        wish_lists = user.wine_wish.all()
        print(wish_lists)
        wine_list = []
        for wish_list in wish_lists:
            # print(wish_list)
            wine_id = wish_list.id
            # print(wine_id)  # 숫자 키 값
            wine = WineModel.objects.get(id=wine_id)
            wine_list.append(wine)

        print(wine)            
        print(wine_list)
        return render(request, 'user/my_wish.html', {'wine_list': wine_list})

# 찜 목록 추가하기
# id = wine_id, number
@login_required
def post_wish(request, id):
    wine = WineModel.objects.get(id=id)
    user = request.user
    click_wish = user.wine_wish.all()
    if wine in click_wish:
        user.wine_wish.remove(wine)
    else:
        user.wine_wish.add(wine)
    return redirect('users:get_wish', user.id)
    # if number == 100:
    #     return redirect('wines:detail', user.id)
    # else:
    #     return redirect('users:post_wish', user.id)