from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, ProductViewSet, CartViewSet, CartItemViewSet, TelegramUserViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'telegram-users', TelegramUserViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('fidda-store/', include(router.urls)),
]