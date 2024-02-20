from django.contrib.auth.models import AbstractUser
from django.db import models


class ApiUser(AbstractUser):
    TYPE_CHOICES = (
        ('Поставщик', 'Поставщик'),
        ('Потребитель', 'Потребитель'),
    )
    user_type = models.CharField(max_length=20, choices=TYPE_CHOICES)


class Warehouse(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.PositiveIntegerField()
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    warehouse = models.ForeignKey(Warehouse, related_name="product", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.warehouse.name}. name: {self.name}, price: {self.price}, description: {self.description}. quantity: {self.quantity}"


class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(ApiUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
