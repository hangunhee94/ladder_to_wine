from http.client import HTTP_PORT
from django.shortcuts import render, redirect
from .models import UserModel
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
    return redirect('/')