from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
CATEGORY = (
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Kids', 'Kids'),
    ('Accessories', 'Accessories'),
)

SIZE_CHOICES = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    ('Universal', 'Universal'),
)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, null=True)
    color = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.size} - {self.color}'


class Order(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=(
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ), default='Pending')

    def __str__(self):
        return f'{self.customer}-{self.name}'
