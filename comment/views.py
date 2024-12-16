from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Comment, Reaction


@login_required(login_url=settings.LOGIN_URL)
def add_comment(request, app_label, model_name, object_id, parent_id=None):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = object_id
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                if parent_comment.content_type == comment.content_type:
                    comment.parent = parent_comment
            comment.save()
            messages.success(request, "Comment added successfully!")
        else:
            messages.error(request, "Failed to add comment. Please try again.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url=settings.LOGIN_URL)
def update_comment(request, comment_id):
    comment = Comment.objects.filter(pk=comment_id).first()
    if comment and request.method == "POST":
        form = CommentForm(data=request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully!")
        else:
            messages.error(request, "Failed to update comment. Please try again.")
    else:
        messages.warning(request, "Comment not found or invalid request.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    form = CommentForm(instance=comment)
    return render(request, "comment/update_comment.html", {"form": form})


@login_required(login_url=settings.LOGIN_URL)
def delete_comment(request, comment_id):
    comment = Comment.objects.filter(pk=comment_id).first()

    if comment and request.user == comment.user:
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
    else:
        messages.error(request, "Failed to delete comment. You are not authorized to perform this action.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url=settings.LOGIN_URL)
def add_reaction(request, comment_id, reaction_type):
    """Handle a like or dislike reaction on a comment.
    If a user reacts with the same type, it removes their reaction (toggle).
    If switching between like and dislike, adjust the like count accordingly.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    try:
        # Fetch existing reaction, or create a new one
        reaction = Reaction.objects.get(user=request.user, comment=comment)
        # Check if the user is toggling their reaction
        if reaction.reaction_type == reaction_type:
            # If the same type is clicked again, remove reaction
            if reaction_type == "like":
                comment.like_count -= 1
            elif reaction_type == "dislike":
                comment.like_count += 1

            reaction.delete()
            messages.success(request, "Reaction removed successfully!")
        else:
            # If switching from like to dislike or vice versa, adjust counts accordingly
            if reaction_type == "like":
                comment.like_count += 1
            elif reaction_type == "dislike":
                comment.like_count -= 1
            reaction.reaction_type = reaction_type
            reaction.save()
            messages.success(request, "Reaction updated successfully!")
    except Reaction.DoesNotExist:
        # No prior reaction, create one
        reaction = Reaction.objects.create(user=request.user, comment=comment, reaction_type=reaction_type)
        if reaction_type == "like":
            comment.like_count += 1
        elif reaction_type == "dislike":
            comment.like_count -= 1
        messages.success(request, "Reaction added successfully!")

    # Save the like_count change
    comment.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))
