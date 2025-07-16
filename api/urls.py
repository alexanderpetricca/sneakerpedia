from django.urls import path

from rest_framework.routers import SimpleRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import views


router = SimpleRouter()
router.register('brands', views.BrandViewSet, basename='brands')
router.register('sneakers', views.SneakerViewSet, basename='sneakers')


urlpatterns = router.urls

spectacular_patterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += spectacular_patterns