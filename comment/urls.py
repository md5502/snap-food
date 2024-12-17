from django.urls import path

from .views import add_comment, add_reaction, delete_comment

app_name = "comment"


urlpatterns = [
    path(
        "add/<str:app_label>/<str:model_name>/<uuid:object_id>/",
        add_comment,
        name="add_comment",
    ),
    path(
        "add/<str:app_label>/<str:model_name>/<uuid:object_id>/<int:parent_id>/",
        add_comment,
        name="add_reply",
    ),
    path(
        "delete/<int:comment_id>/",
        delete_comment,
        name="delete_comment",
    ),
    path(
        "react/<int:comment_id>/<str:reaction_type>",
        add_reaction,
        name="add_reaction",
    ),

]
