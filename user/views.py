from http.client import HTTP_PORT
from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        nickname = request.POST.get('nickname', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if password != password2:
            return render(request, 'signup.html')
        else:
            exist_user = UserModel.objects.filter(username=username)

            if exist_user:
                return render(request, 'signup.html')
            else:
                new_user = UserModel()
                new_user.username = username
                new_user.nickname = nickname
                new_user.password = password
                new_user.save()
                return redirect('/sign-in')

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        me = UserModel.objects.get(username=username)
        if me.password == password:
            request.session['user'] = me.username
            return HttpResponse(me.nickname + "님 환영합니다.")
        else:
            return redirect('/sign-in')

    elif request.method == 'GET':
        return render(request, 'signin.html')