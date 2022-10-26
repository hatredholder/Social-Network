from django.shortcuts import redirect, render


def home_view(request):
    """
    Welcoming page view, redirects to the board if user is authenticated.
    """
    if request.user.is_authenticated:
        return redirect("posts/")
    return render(request, "main/home.html")
