from rest_framework import serializers

from .models import Product

def validate_title(value):
    qs = Product.objects.filter(title__iexact=value) # key sensitive
    if qs.exists():
        raise serializers.ValidationError(f"{value} is already a product name")
    return value