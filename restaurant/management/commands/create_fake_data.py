import random
from datetime import time

import factory
from django.core.management.base import BaseCommand
from faker import Faker

from food.models import Food
from menu.models import DayOfWeek, Menu
from restaurant.models import Restaurant
from users.models import CustomUser

faker = Faker()

# CustomUser Factory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.LazyAttribute(lambda _: faker.unique.email())
    password = factory.PostGenerationMethodCall("set_password", "password123")

# DayOfWeek Factory
class DayOfWeekFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DayOfWeek

    day = factory.Iterator(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

# Restaurant Factory
class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.LazyAttribute(lambda _: faker.company())
    logo = "restaurants/default.jpg"
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=200))
    owner = factory.SubFactory(UserFactory)
    address = factory.LazyAttribute(lambda _: faker.address())
    call_number = factory.LazyAttribute(lambda _: faker.phone_number())
    rate = factory.LazyAttribute(lambda _: random.choice(["1", "2", "3", "4", "5"]))
    time_to_open = factory.LazyAttribute(lambda _: time(hour=random.randint(6, 11)))
    time_to_close = factory.LazyAttribute(lambda _: time(hour=random.randint(17, 23)))

# Food Factory
class FoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Food

    name = factory.LazyAttribute(lambda _: faker.word().capitalize())
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=100))
    image = "foods/default.jpg"
    count = factory.LazyAttribute(lambda _: random.randint(10, 100))
    rate = factory.LazyAttribute(lambda _: random.choice(["1", "2", "3", "4", "5"]))
    discount = factory.LazyAttribute(lambda _: random.randint(0, 50))
    price = factory.LazyAttribute(lambda _: random.randint(1000, 50000))
    restaurant = factory.SubFactory(RestaurantFactory)

# Menu Factory
class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    name = factory.LazyAttribute(lambda _: faker.word().capitalize())
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=100))
    restaurant = factory.SubFactory(RestaurantFactory)
    available_from = factory.LazyAttribute(lambda _: time(hour=random.randint(9, 12)))
    available_to = factory.LazyAttribute(lambda _: time(hour=random.randint(13, 20)))
    is_active = factory.LazyAttribute(lambda _: random.choice([True, False]))

    @factory.post_generation
    def available_days(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for day in extracted:
                self.available_days.add(day)
        else:
            self.available_days.add(*DayOfWeek.objects.all()[:3])

    @factory.post_generation
    def foods(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for food in extracted:
                self.foods.add(food)
        else:
            self.foods.add(*Food.objects.all()[:5])

# Command class for managing command execution
class Command(BaseCommand):
    help = "Create fake data for the application"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating fake data...")

        # ایجاد کاربران
        users = UserFactory.create_batch(5)

        # ایجاد روزهای هفته
        days = [DayOfWeekFactory(day=day) for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]]

        # ایجاد رستوران‌ها و منوها
        for _ in range(10):
            restaurant = RestaurantFactory()
            menus = MenuFactory.create_batch(3, restaurant=restaurant)
            foods = FoodFactory.create_batch(10, restaurant=restaurant)

            # افزودن روزها و غذاها به منو
            for menu in menus:
                menu.available_days.set(random.sample(days, k=random.randint(1, 7)))
                menu.foods.set(random.sample(foods, k=random.randint(1, 5)))

        self.stdout.write(self.style.SUCCESS("Fake data created successfully!"))
