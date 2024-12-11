from django.core.exceptions import ValidationError
from django.db import models

from common.models import BaseModel
from restaurant.models import Restaurant
from users.models import CustomUser


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




class FoodComment(BaseModel):
    user = models.ForeignKey(
        CustomUser,
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
