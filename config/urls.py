from allauth.account.views import ConfirmEmailView, EmailVerificationSentView
from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    path("admin/", admin.site.urls),

    path("accounts/", include("allauth.urls")),
    path("accounts/", include("users.urls")),

    path("comments/", include("comment.urls")),

    path("restaurant-dashboard/", include("restaurant.urls")),
    path("restaurant-dashboard/", include("food.urls")),
    path("restaurant-dashboard/", include("menu.urls")),
    path("api/restaurant-dashboard/", include("restaurant.api.urls")),
    path("api/restaurant-dashboard/", include("food.api.urls")),
    path("api/restaurant-dashboard/", include("menu.api.urls")),

    path("api/auth/", include("dj_rest_auth.urls")),

    path(
        "api/auth/registration/account-email-verification-sent/",
        EmailVerificationSentView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "api/auth/password/reset/confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "api/auth/registration/account-confirm-email/<str:key>/",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),

    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
