from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from config.settings import LOGIN_URL

from .forms import AddressForm, UpdateUserProfileFrom
from .models import Address, UserProfile


@login_required(login_url=LOGIN_URL)
def user_profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    return render(request, "users/profile.html", {"profile": userprofile})


@login_required(login_url=LOGIN_URL)
def edit_user_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UpdateUserProfileFrom(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "user profile update successfully")
            return redirect("/accounts/profile/")

    form = UpdateUserProfileFrom(instance=userprofile)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required(login_url=LOGIN_URL)
def create_address(request):
    if request.user.addresses.count() >= 3:  # noqa: PLR2004
        messages.error(request, "You can't add more than 3 addresses.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            form.save_m2m()
            messages.success(request, "address added successfully")
            return redirect(request.META.get("HTTP_REFERER", "/"))

    form = AddressForm()
    return render(request, "users/create_address.html", {"form": form})

@login_required(login_url=LOGIN_URL)
def update_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "address update successfully")
            return redirect(request.META.get("HTTP_REFERER", "/"))

    form = AddressForm(instance=address)
    return render(request, "users/create_address.html", {"form": form})


@login_required(login_url=LOGIN_URL)
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if address.user == request.user:
        address.delete()
        messages.success(request, "address delete successfully")
    return redirect(request.META.get("HTTP_REFERER", "/"))
