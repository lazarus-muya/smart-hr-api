from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
# from rest_framework_jwt.blacklist.views import BlacklistView


urlpatterns = [
    path("admin/", admin.site.urls),

    # auth urls
    path('api-token/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    # path("auth/", obtain_jwt_token),
    # path("auth/logout/", BlacklistView.as_view({"post": "create"})),

    # api urls
    path("api/", include("api.urls")),
    path("api/auth/", include("src.authentication.urls")),
    path("api/recruitment/", include("src.recruitment.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
