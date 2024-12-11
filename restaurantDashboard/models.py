from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from common.models import BaseModel
from users.models import CustomUser


class Restaurant(BaseModel):
    RATE_CHOSES = (
        ("1", "very bad"),
        ("2", "bad"),
        ("3", "natural"),
        ("4", "good"),
        ("5", "very good"),
    )
    name = models.CharField(max_length=120)
    logo = models.ImageField(default="restaurants/default.jpg", upload_to="restaurants")
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="restaurants")
    address = models.CharField(max_length=1000)
    call_number = models.CharField(max_length=16)
    rate = models.CharField(max_length=1, choices=RATE_CHOSES, default=RATE_CHOSES[4][0])
    time_to_open = models.TimeField()
    time_to_close = models.TimeField()

    def clean(self):
        if self.time_to_close <= self.time_to_open:
            raise ValidationError({"time_to_close": "Closing time must be after opening time."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail_restaurant", kwargs={"pk": self.id})

    def __str__(self):
        return self.name


class Food(BaseModel):
    RATE_CHOSES = (
        ("1", "very bad"),
        ("2", "bad"),
        ("3", "natural"),
        ("4", "good"),
        ("5", "very good"),
    )

    name = models.CharField(max_length=120)
    description = models.TextField()

    image = models.ImageField(default="foods/default.jpg", upload_to="foods")
    count = models.PositiveIntegerField()
    rate = models.CharField(max_length=1, choices=RATE_CHOSES, default=RATE_CHOSES[4][0])
    discount = models.PositiveIntegerField(default=0)
    price = models.PositiveBigIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="foods")

    def clean(self):
        if self.discount <= 0 and self.discount >= 99:  # noqa: PLR2004
            raise ValidationError({"discount": "Discount should start from 0 to 99"})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DayOfWeek(BaseModel):
    DAY_CHOICES = (
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    )
    day = models.CharField(max_length=3, choices=DAY_CHOICES, unique=True)

    def __str__(self):
        return self.get_day_display()


class Menu(BaseModel):
    name = models.CharField(max_length=120)
    description = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    foods = models.ManyToManyField(Food, related_name="menus", blank=True)
    available_from = models.TimeField()
    available_to = models.TimeField()
    is_active = models.BooleanField(default=True)
    available_days = models.ManyToManyField(DayOfWeek, related_name="menus")

    def clean(self):
        if self.available_from >= self.available_to:
            raise ValidationError({"available_to": "The end time must be after the start time."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"


class RestaurantComment(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="restaurant_comments",
    )
    text = models.TextField()
    restaurant = models.ForeignKey(
        "Restaurant",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.restaurant}"


class RestaurantCommentLike(BaseModel):
    """Store unique likes for each user on a comment.
    Prevents multiple likes on the same comment by the same user.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="restaurant_comment_likes",
    )
    comment = models.ForeignKey(
        RestaurantComment,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment")  # Prevent multiple likes on the same comment by the same user

class RestaurantCommentDislike(BaseModel):
    """Store unique likes for each user on a comment.
    Prevents multiple likes on the same comment by the same user.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="restaurant_comment_dislikes",
    )
    comment = models.ForeignKey(
        RestaurantComment,
        on_delete=models.CASCADE,
        related_name="dislikes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment")  # Prevent multiple likes on the same comment by the same user


class FoodComment(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="food_comments",
    )
    text = models.TextField()
    food = models.ForeignKey(
        "Food",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.food}"


class FoodCommentLike(BaseModel):
    """Store unique likes for each user on a comment.
    Prevents multiple likes on the same comment by the same user.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="food_comment_likes",
    )
    comment = models.ForeignKey(
        FoodComment,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment")  # Prevent multiple likes on the same comment by the same user

class FoodCommentDislike(BaseModel):
    """Store unique likes for each user on a comment.
    Prevents multiple likes on the same comment by the same user.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="food_comment_dislikes",
    )
    comment = models.ForeignKey(
        FoodComment,
        on_delete=models.CASCADE,
        related_name="dislikes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment")  # Prevent multiple likes on the same comment by the same user
