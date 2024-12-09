from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from config.settings import LOGIN_URL

from .forms import UpdateUserProfileFrom
from .models import UserProfile


@login_required(login_url=LOGIN_URL)
def user_profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    return render(request, "users/profile.html", {"profile": userprofile})


@login_required(login_url=LOGIN_URL)
def edit_user_profile(request):

    userprofile = get_object_or_404(UserProfile, user = request.user)
    if request.method == "POST":
        form = UpdateUserProfileFrom(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            return redirect("/accounts/profile/")

    form = UpdateUserProfileFrom(instance=userprofile)
    return render(request, "users/edit_profile.html", {"form": form})

