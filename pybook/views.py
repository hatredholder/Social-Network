


from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def home_view(request):
    if request.user.is_authenticated:
        return redirect('posts/')
    return render(request, 'main/home.html')