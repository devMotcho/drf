from rest_framework import serializers
from rest_framework.reverse import reverse
from api.serializers import UserPublicSerializer

from .models import Product
from . import validators

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    my_user_data = serializers.SerializerMethodField(read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        )
    #email = serializers.EmailField(write_only=True)
    title = serializers.CharField(validators=[
        validators.validate_title_no_hello,
        validators.unique_product_title,
        ])
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Product
        fields = [
            'owner', #id
            'email',
            'url',
            'edit_url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount',
            'my_user_data',
        ]
    def get_my_user_data(self, obj):
       return {
            "username": obj.user.username
        }
    
    # def validate_title(self, value):
    #     qs = Product.objects.filter(title__iexact=value) # key sensitive
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value
    
    # def create(self, validated_data):
    #     return super().create(validated_data)
    
    # def update(self, instance, validated_data)        }:
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