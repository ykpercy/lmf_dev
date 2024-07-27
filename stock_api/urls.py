from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockSpotViewSet

router = DefaultRouter()
router.register(r'stock-spot', StockSpotViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]