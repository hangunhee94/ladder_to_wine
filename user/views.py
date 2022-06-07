from django.shortcuts import render, redirect
from .models import UserModel

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
            new_user = UserModel()
            new_user.username = username
            new_user.nickname = nickname
            new_user.password = password
            new_user.save()
            
        return redirect('/sign-in')

def sign_in_view(request):
    return render(request, 'signin.html')