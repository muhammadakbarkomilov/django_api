from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Telegram_User, Order


# Telegram User Serializer
class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telegram_User
        fields = '__all__'


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


# CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = '__all__'