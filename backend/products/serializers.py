from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product

from .validators import validate_title

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        )
    #email = serializers.EmailField(write_only=True)
    title = serializers.CharField(validators=[validate_title])

    class Meta:
        model = Product
        fields = [
            'url',
            'edit_url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount',
        ]
    
    # def validate_title(self, value):
    #     qs = Product.objects.filter(title__iexact=value) # key sensitive
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value
    
    # def create(self, validated_data):
    #     return super().create(validated_data)
    
    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #       ....
    #     return super().update(instance, validated_data)

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)
    
    def get_my_discount(self, obj):
        return obj.get_discount()