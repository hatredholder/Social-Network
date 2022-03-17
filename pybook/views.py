


from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    user = request.user
    context = {
        'user':user,
    }
    return render(request, 'main/home.html', context)