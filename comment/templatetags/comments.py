from django import template
from django.contrib.contenttypes.models import ContentType

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag("comment/list_comments_admin.html")
def list_comments_admin(obj, request):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.id).order_by("-created_at")
    comment_list = []
    for comment in comments:
        reactions = comment.reactions
        like_count = reactions.filter(reaction_type="like").count()
        dislike_count = reactions.filter(reaction_type="dislike").count()
        object = {}
        object["content"] = comment.content
        object["user"] = comment.user
        object["created_at"] = comment.created_at
        object["like_count"] = like_count
        object["dislike_count"] = dislike_count
        object["object_id"] = comment.object_id
        object["id"] = comment.pk
        comment_list.append(object)
    return {
        "request": request,
        "comments": comment_list,
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
