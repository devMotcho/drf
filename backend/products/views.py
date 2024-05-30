from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .models import Product
from api.mixins import (
    StaffEditorPermissionMixin,
    UserQuerysetMixin,
    )
from .serializers import ProductSerializer




class ProductListCreateAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    """
    List and
    Create a product,
    if content is none content = title
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # ---- ADDED DEFAULT TO settings.py ------

    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication,
    #     ]
    
    # ---- ADDED MIXIN TO api.mixins.py ------

    # permission_classes = [
    #     permissions.IsAdminUser,
    #     IsStaffEditorPermission,
    #     ]

    # IsAuthenticatedOrReadOnly -> can only read
    # IsAuthenticated -> Need be authenticated
    # DjangoModelPermissions -> Group Permissions
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)
        return super().perform_create(serializer)
    
    #  Subsituido por UserQuerysetMixin
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=request.user)


class ProductDetailAPIView(
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    """
    Get one single product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk' -> int

class ProductUpdateAPIView(
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    """
    Update one single product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

        return super().perform_update(serializer)

class ProductDestroyAPIView(
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    """
    Delete one single product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        #instance
        return super().perform_destroy(instance)


# Mixins
class ProductMixinView(
    StaffEditorPermissionMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' # list dont care about this.

    #HTTP -> get 
    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")
        # Detail view
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        # List View
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(content=content)
        return super().perform_create(serializer)

# class ProductListAPIView(generics.ListAPIView):
#     """
#     Not gonna use
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'pk' -> int

# function way to do Mixin
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            #detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    
    if method == "POST":
        # create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"Invalid": "not good data"}, status=400)
    



