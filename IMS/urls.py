"""
URL configuration for IMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static 
from app1.urls import router
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Inventory Management System APIs",
        default_version= "v1",
        description="Coming soon",
        terms_of_service="https://ww.goggle.com/policies/terms/",
        contact = openapi.Contact(email="ngagadancan2003@gmail.com"),
        license = openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^__debug__/", include(debug_toolbar.urls)),

    #re_path(r"^swagger", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),




    path('', include('app.urls')),
    path('', include('image.urls')),
    path('', include('app1.urls')),
    path('', include('reports.urls')),

    path("api/", include(router.urls)),

    path("api-auth/", include("rest_framework.urls")),
] + static(settings.STATIC_URL,
                       document_root = settings.STATIC_ROOT) + static(
                           settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
                       )





