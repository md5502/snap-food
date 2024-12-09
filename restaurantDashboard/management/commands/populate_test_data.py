import random

from django.core.management.base import BaseCommand
from faker import Faker

from restaurantDashboard.models import DayOfWeek, Food, FoodComment, Menu, Restaurant, RestaurantComment
from users.models import CustomUser

faker = Faker()

class Command(BaseCommand):
    help = "Populate the database with fake data for testing"

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_restaurants_and_foods()
        self.create_menus()
        self.create_comments()

    def create_users(self):
        for _ in range(10):  # Create 10 users
            CustomUser.objects.create_user(
                email=faker.email(),
                password="password123",
            )
        self.stdout.write("Created 10 users.")

    def create_restaurants_and_foods(self):
        users = CustomUser.objects.all()
        for _ in range(5):  # Create 5 restaurants
            owner = random.choice(users)
            restaurant = Restaurant.objects.create(
                name=faker.company(),
                logo="uploads/restaurants/default.jpg",
                description=faker.text(),
                owner=owner,
                address=faker.address(),
                call_number=faker.phone_number(),
                rate=random.choice([r[0] for r in Restaurant.RATE_CHOSES]),
                time_to_open="08:00:00",
                time_to_close="20:00:00",

            )
            for _ in range(random.randint(5, 10)):  # Create 5-10 foods per restaurant
                Food.objects.create(
                    name=faker.word(),
                    image="uploads/foods/default.jpg",
                    count=random.randint(10, 100),
                    rate=random.choice([r[0] for r in Food.RATE_CHOSES]),
                    discount=random.randint(0, 30),
                    price=random.randint(50, 500) * 1000,
                    restaurant=restaurant,
                )
        self.stdout.write("Created 5 restaurants and their foods.")

    def create_menus(self):
        restaurants = Restaurant.objects.all()
        for restaurant in restaurants:
            for _ in range(2):  # Create 2 menus per restaurant
                menu = Menu.objects.create(
                    name=faker.word(),
                    description=faker.text(),
                    restaurant=restaurant,
                    available_from="08:00:00",  # Fixed start time
                    available_to="20:00:00",
                    is_active=random.choice([True, False]),
                )
                foods = Food.objects.filter(restaurant=restaurant)
                menu.foods.set(random.sample(list(foods), min(3, len(foods))))  # Add 3 foods to each menu
                menu.available_days.set(DayOfWeek.objects.all()[:3])  # Assign first 3 days
        self.stdout.write("Created menus for each restaurant.")

    def create_comments(self):
        users = CustomUser.objects.all()
        restaurants = Restaurant.objects.all()
        foods = Food.objects.all()

        for restaurant in restaurants:
            for _ in range(random.randint(1, 5)):  # Create 1-5 comments per restaurant
                RestaurantComment.objects.create(
                    user=random.choice(users),
                    text=faker.text(),
                    restaurant=restaurant,
                    like_count=random.randint(0, 50),
                    dislike_count=random.randint(0, 20),
                )

        for food in foods:
            for _ in range(random.randint(1, 5)):  # Create 1-5 comments per food
                FoodComment.objects.create(
                    user=random.choice(users),
                    text=faker.text(),
                    restaurant=food,
                    like_count=random.randint(0, 50),
                    dislike_count=random.randint(0, 20),
                )
        self.stdout.write("Created comments for restaurants and foods.")

