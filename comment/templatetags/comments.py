from django import template
from django.contrib.contenttypes.models import ContentType

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag("comment/list_comment.html")
def list_comments(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.id).order_by("-created_at")

    return {
        "comments": comments,
        "model_name": obj._meta.model_name,
        "app_label": obj._meta.app_label,
    }


@register.inclusion_tag("comment/comment_form.html")
def comment_form(obj, user=None):
    return {
        "form": CommentForm(),
        "object_id": obj.pk,
        "app_label": obj._meta.app_label,
        "model_name": obj._meta.model_name,
        "user": user,
    }
