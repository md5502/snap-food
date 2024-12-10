from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from config.settings import LOGIN_URL
from restaurantDashboard.forms import RestaurantCommentForm, RestaurantForm
from restaurantDashboard.models import Restaurant, RestaurantComment


class RestaurantListView(LoginRequiredMixin, ListView):
    model = Restaurant
    template_name = "restaurantDashboard/restaurant_list.html"

    def get_queryset(self):
        restaurants = get_list_or_404(Restaurant, owner=self.request.user)
        return restaurants


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    model = Restaurant
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurant_dashboard:list_restaurant")

    def form_valid(self, form):
        restaurant = form.save(commit=False)
        restaurant.owner = self.request.user
        restaurant.save()
        form.save_m2m()
        messages.success(self.request, "Restaurant create susseccfully")

        return super().form_valid(form)


class RestaurantDetailView(LoginRequiredMixin, DetailView):
    model = Restaurant

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["comment_form"] = RestaurantCommentForm()
        context["obj"] = self.get_object()
        context["comments"] = RestaurantComment.objects.filter(restaurant=self.get_object()).select_related("user")
        return context


class RestaurantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantForm

    def form_valid(self, form):
        messages.success(self.request, "The restaurant was updated successfully.")
        return super().form_valid(form)

    def test_func(self):
        restaurant = self.get_object()
        if restaurant.owner == self.request.user:
            return True
        messages.warning(self.request, "This restaurant is not yours to update.")
        return False

    def get_success_url(self):
        return reverse_lazy("restaurant_dashboard:detail_restaurant", kwargs={"pk": self.object.pk})


class RestaurantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Restaurant
    success_url = reverse_lazy("restaurant_dashboard:list_restaurant")

    def test_func(self):
        restaurant = self.get_object()
        return self.request.user == restaurant.owner

    def handle_no_permission(self):
        messages.warning(self.request, "This restaurant is not yours to delete.")
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Restaurant deleted.")
        return super().delete(request, *args, **kwargs)


class RestaurantCommentCreateView(LoginRequiredMixin, CreateView):
    model = RestaurantComment
    form_class = RestaurantCommentForm

    def form_valid(self, form):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs.get("pk"))
        form.instance.user = self.request.user
        form.instance.restaurant = restaurant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("restaurant_dashboard:detail_restaurant", kwargs={"pk": self.kwargs.get("pk")})


class RestaurantCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RestaurantComment
    form_class = RestaurantCommentForm

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def get_success_url(self):
        return reverse("restaurant_dashboard:detail_restaurant", kwargs={"pk": self.object.restaurant.pk})


class RestaurantCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RestaurantComment

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def get_success_url(self):
        return reverse("restaurant_dashboard:detail_restaurant", kwargs={"pk": self.object.restaurant.pk})


@login_required(login_url=LOGIN_URL)
def restaurant_comment_like_view(request, comment_pk):
    comment = get_object_or_404(RestaurantComment, pk=comment_pk)
    restaurant_pk = comment.restaurant.pk
    comment.like_count += 1
    comment.save()
    return redirect("restaurant_dashboard:detail_restaurant", pk=restaurant_pk)


@login_required(login_url=LOGIN_URL)
def restaurant_comment_dislike_view(request, comment_pk):
    comment = get_object_or_404(RestaurantComment, pk=comment_pk)
    restaurant_pk = comment.restaurant.pk
    comment.dislike_count += 1
    comment.save()
    return redirect("restaurant_dashboard:detail_restaurant", pk=restaurant_pk)


@login_required(login_url=LOGIN_URL)
def restaurant_comment_reply_view(request, parent_comment_pk):
    parent_comment = get_object_or_404(RestaurantComment, pk=parent_comment_pk)
    if request.method == "POST":
        text_replay = request.POST.get("reply_text", "").strip()
        if not text_replay:
            messages.error(request, "Reply text cannot be empty.")
            return redirect("restaurant_dashboard:detail_restaurant", pk=parent_comment.restaurant.pk)

        RestaurantComment.objects.create(
            user=request.user,
            text=text_replay,
            restaurant=parent_comment.restaurant,  # Parent's restaurant is used
            parent=parent_comment,  # Set parent comment
        )
        messages.success(request, "Your reply has been added.")
        return redirect("restaurant_dashboard:detail_restaurant", pk=parent_comment.restaurant.pk)
    messages.error(request, "Invalid request method.")
    return redirect("restaurant_dashboard:detail_restaurant", pk=parent_comment.restaurant.pk)
