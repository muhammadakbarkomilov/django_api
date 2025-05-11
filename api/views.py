from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Category, Product, Cart, CartItem, Telegram_User, Order
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, TelegramUserSerializer, OrderSerializer

# Telegram User ViewSet
class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = Telegram_User.objects.all()
    serializer_class = TelegramUserSerializer

    @action(detail=True, methods=['get'])
    def cart(self, request, pk=None):
        telegram_user = self.get_object()
        cart = Cart.objects.filter(telegram_user=telegram_user).last()
        if cart:
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)
        else:
            return Response({"message": "Savat mavjud emas"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        telegram_user = self.get_object()
        orders = Order.objects.filter(cart__telegram_user=telegram_user)
        order_serializer = OrderSerializer(orders, many=True)
        return Response(order_serializer.data)


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Cart ViewSet
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        cart = self.get_object()
        return Response(cart.get_cart_details())

    @action(detail=True, methods=['get'])
    def total_items(self, request, pk=None):
        cart = self.get_object()
        return Response({'total_items': cart.total_items()})

    @action(detail=True, methods=['get'])
    def total_price(self, request, pk=None):
        cart = self.get_object()
        return Response({'total_price': cart.total_price()})

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        cart, created = Cart.objects.get_or_create(user=user)

        items_data = data.get('items', [])
        for item in items_data:
            product = Product.objects.get(id=item['product'])
            CartItem.objects.create(cart=cart, product=product, quantity=item['quantity'])

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        cart = self.get_object()
        data = request.data
        items_data = data.get('items', [])

        # Kartadagi barcha elementlarni yangilash
        cart.items.clear()
        for item in items_data:
            product = Product.objects.get(id=item['product'])
            CartItem.objects.create(cart=cart, product=product, quantity=item['quantity'])

        serializer = CartSerializer(cart)
        return Response(serializer.data)


# CartItem ViewSet
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        product = Product.objects.get(id=data['product'])
        cart = Cart.objects.get(id=data['cart'])
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=data['quantity'])
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.quantity = request.data['quantity']
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['get'])
    def total_price(self, request, pk=None):
        order = self.get_object()
        return Response({'total_price': order.total_price()})