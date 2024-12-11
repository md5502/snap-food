from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from config.settings import LOGIN_URL
from restaurantDashboard.forms import FoodCommentForm, FoodForm
from restaurantDashboard.models import Food, FoodComment, FoodCommentDislike, FoodCommentLike, Restaurant


class FoodListView(LoginRequiredMixin, ListView):
    model = Food

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs["restaurant_id"])
        return Food.objects.filter(restaurant=restaurant)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["res_id"] = self.kwargs["restaurant_id"]
        return context


class FoodDetailView(LoginRequiredMixin, DetailView):
    model = Food

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["food_comment_form"] = FoodCommentForm()
        context["obj"] = self.get_object()
        context["comments"] = FoodComment.objects.filter(food=self.get_object()).select_related("user")

        return context


class FoodCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Food
    form_class = FoodForm

    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=kwargs["restaurant_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        food = form.save(commit=False)
        food.restaurant = self.restaurant
        food.save()
        form.save_m2m()
        messages.success(self.request, "Food created successfully.")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.restaurant.owner

    def handle_no_permission(self):
        messages.warning(self.request, "You are not authorized to create food for this restaurant.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse_lazy("restaurant_dashboard:food_list", kwargs={"restaurant_id": self.kwargs["restaurant_id"]})


class FoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Food
    form_class = FoodForm

    def form_valid(self, form):
        messages.success(self.request, "The food was updated successfully.")
        return super().form_valid(form)

    def test_func(self):
        food = self.get_object()
        return self.request.user == food.restaurant.owner

    def handle_no_permission(self):
        messages.warning(self.request, "This food is not yours to update.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse_lazy("restaurant_dashboard:food_detail", kwargs={"pk": self.get_object().pk})


class FoodDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Food

    def test_func(self):
        food = self.get_object()
        return self.request.user == food.restaurant.owner

    def handle_no_permission(self):
        messages.warning(self.request, "This food is not yours to delete.")
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Food deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        food = self.get_object()
        return reverse_lazy("restaurant_dashboard:food_list", kwargs={"restaurant_id": food.restaurant.pk})


class FoodCommentCreateView(LoginRequiredMixin, CreateView):
    model = FoodComment
    form_class = FoodCommentForm

    def form_valid(self, form):
        food = get_object_or_404(Food, pk=self.kwargs.get("pk"))
        form.instance.user = self.request.user
        form.instance.food = food
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("restaurant_dashboard:food_detail", kwargs={"pk": self.kwargs.get("pk")})


class FoodCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FoodComment
    form_class = FoodCommentForm

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def get_success_url(self):
        return reverse("restaurant_dashboard:food_detail", kwargs={"pk": self.object.restaurant.pk})


class FoodCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FoodComment

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def get_success_url(self):
        return reverse("restaurant_dashboard:food_detail", kwargs={"pk": self.object.restaurant.pk})


@login_required(login_url=LOGIN_URL)
def food_comment_like_view(request, comment_pk):
    comment = get_object_or_404(FoodComment, pk=comment_pk)
    food_pk = comment.food.pk
    user = request.user
    like_comment = FoodCommentLike.objects.filter(comment=comment).first()

    if like_comment and user == like_comment.user:
        messages.info(request, "you already like this comment ")
        return redirect("restaurant_dashboard:food_detail", pk=food_pk)

    FoodCommentLike.objects.create(user=user, comment=comment)
    comment.like_count += 1
    comment.save()
    return redirect("restaurant_dashboard:food_detail", pk=food_pk)


@login_required(login_url=LOGIN_URL)
def food_comment_dislike_view(request, comment_pk):
    comment = get_object_or_404(FoodComment, pk=comment_pk)
    food_pk = comment.food.pk
    user = request.user
    dislike_comment = FoodCommentDislike.objects.filter(comment=comment).first()
    if dislike_comment and user == dislike_comment.user:
        messages.info(request, "you already dislike this comment ")
        return redirect("restaurant_dashboard:food_detail", pk=food_pk)

    FoodCommentDislike.objects.create(user=user, comment=comment)
    comment.dislike_count += 1
    comment.save()
    return redirect("restaurant_dashboard:food_detail", pk=food_pk)



@login_required(login_url=LOGIN_URL)
def food_comment_reply_view(request, parent_comment_pk):
    parent_comment = get_object_or_404(FoodComment, pk=parent_comment_pk)
    if request.method == "POST":
        text_replay = request.POST.get("reply_text", "").strip()
        if not text_replay:
            messages.error(request, "Reply text cannot be empty.")
            return redirect("restaurant_dashboard:food_detail", pk=parent_comment.food.pk)

        FoodComment.objects.create(
            user=request.user,
            text=text_replay,
            food=parent_comment.food,  # Parent's restaurant is used
            parent=parent_comment,  # Set parent comment
        )
        messages.success(request, "Your reply has been added.")
        return redirect("restaurant_dashboard:food_detail", pk=parent_comment.food.pk)
    messages.error(request, "Invalid request method.")
    return redirect("restaurant_dashboard:food_detail", pk=parent_comment.food.pk)
