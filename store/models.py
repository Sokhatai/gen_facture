from django.db import models
from django.urls import reverse
from django.utils import timezone

from shop.settings import AUTH_USER_MODEL

# Create your models here.
"""

Product : 
- Nom
- Prix
- La quantité en stock
- La date de péremption
- Description

"""

class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)
    peremption_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
    
    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})


# Article (Order)(Product qui sera mis dans le panier)

"""
-Utilisateur
-Produit
-Quantité
-Commandé ou non
"""

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    

# Panier (Cart)

"""
-Utilisateur
-Articles
"""

class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username
    
    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)


#Facture

"""

Utilisateur
Articles
Prix Total
Date de la création

"""

class Bill(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ManyToManyField(Order)
    totalPrice = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} {self.created_at}"