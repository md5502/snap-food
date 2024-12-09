from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from restaurantDashboard.forms import MenuForm
from restaurantDashboard.models import Menu, Restaurant


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs["restaurant_id"])
        return Menu.objects.filter(restaurant=restaurant)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["res_id"] = self.kwargs["restaurant_id"]
        return context


class MenuCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Menu
    form_class = MenuForm

    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=kwargs["restaurant_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        menu = form.save(commit=False)
        menu.restaurant = self.restaurant
        menu.save()
        form.save_m2m()

        messages.success(self.request, "Menu created successfully.")
        return super().form_valid(form)

    def test_func(self):
        return self.restaurant.owner == self.request.user

    def handle_no_permission(self):
        messages.warning(self.request, "You are not authorized to create a menu for this restaurant.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse_lazy("restaurant_dashboard:menu_list", kwargs={"restaurant_id": self.kwargs["restaurant_id"]})


class MenuDetailView(LoginRequiredMixin, DetailView):
    model = Menu


class MenuUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Menu
    form_class = MenuForm

    def form_valid(self, form):
        messages.success(self.request, "The menu was updated successfully.")
        return super().form_valid(form)

    def test_func(self):
        menu = self.get_object()
        return self.request.user == menu.restaurant.owner

    def handle_no_permission(self):
        messages.warning(self.request, "This menu is not yours to update.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse_lazy("restaurant_dashboard:menu_detail", kwargs={"pk": self.get_object().pk})


class MenuDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Menu

    def test_func(self):
        menu = self.get_object()
        return self.request.user == menu.restaurant.owner

    def handle_no_permission(self):
        messages.warning(self.request, "This menu is not yours to delete.")
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "menu deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        menu = self.get_object()
        return reverse_lazy("restaurant_dashboard:menu_list", kwargs={"restaurant_id": menu.restaurant.pk})
