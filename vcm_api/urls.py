from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Virtual Contest Maker API",
        default_version="v1.0",
        description='''
        This API provides the necessary backend resources for the
        functioning of Virtual Contest Maker''',
        # TODO: update license, contact, terms of service information(if available)
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path("admin/", admin.site.urls),


    path(
        'api/docs/swagger',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0),
        name='swagger-api-docs'),
    path('api/docs/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-api-docs'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/contests/', include('vcm_api.contest.urls')),

    path('api/users/', include('vcm_api.user.urls')),


]
