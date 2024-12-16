from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import FoodForm
from .models import Food, Restaurant


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
        context["obj"] = self.get_object()

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
        return reverse_lazy("food:food_list", kwargs={"restaurant_id": self.kwargs["restaurant_id"]})


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
        return reverse_lazy("food:food_detail", kwargs={"pk": self.get_object().pk})


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
        return reverse_lazy("food:food_list", kwargs={"restaurant_id": food.restaurant.pk})

