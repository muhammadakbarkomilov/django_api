from django.db import models
from django.contrib.auth.models import User

# Telegram foydalanuvchisi model
class Telegram_User(models.Model):
    tg_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    username = models.CharField(max_length=100)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Kategoriya modeli
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Mahsulot modeli
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


# Savat modeli
class Cart(models.Model):
    telegram_user = models.ForeignKey(Telegram_User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    def __str__(self):
        return f"Savat {self.telegram_user.name} - {self.created_at}"


# Savatdagi mahsulot (CartItem) modeli
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.product.price}"


# Buyurtma modeli
class Order(models.Model):
    cart = models.ForeignKey(Cart, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.total_price() for item in self.cart.cart_items.all())

    def __str__(self):
        return f"Buyurtma {self.id} - {self.status}"