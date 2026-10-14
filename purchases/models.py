from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    picture = models.ImageField(
        upload_to='profiles/',
        null=True
    )

    def __str__(self):
        return self.full_name


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.supplier_name


class Purchase(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    purchase_date = models.DateField()

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    @property
    def total_amount(self):
        return self.subtotal - self.discount

    @property
    def due_amount(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return self.product_name