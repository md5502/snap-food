from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import RestaurantForm
from .models import (
    Restaurant,
)


class RestaurantListView(LoginRequiredMixin, ListView):
    model = Restaurant
    template_name = "restaurant/restaurant_list.html"

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    model = Restaurant
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurant:list_restaurant")

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
        restaurant = self.get_object()
        context["obj"] = restaurant
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
        return reverse_lazy("restaurant:detail_restaurant", kwargs={"pk": self.object.pk})


class RestaurantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Restaurant
    success_url = reverse_lazy("restaurant:list_restaurant")

    def test_func(self):
        restaurant = self.get_object()
        return self.request.user == restaurant.owner

    def handle_no_permission(self):
        messages.warning(self.request, "This restaurant is not yours to delete.")
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Restaurant deleted.")
        return super().delete(request, *args, **kwargs)
