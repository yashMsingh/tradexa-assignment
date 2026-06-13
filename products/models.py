from django.db import models


class Product(models.Model):
    """
    Product model stored in the separate products_db (db_products.sqlite3).
    Routing is handled by AppRouter in tradexa_assignment/db_router.py.
    """
    name = models.CharField(max_length=200)
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Weight in kg",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in INR",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'products'

    def __str__(self):
        return f"{self.name} — ₹{self.price}"
