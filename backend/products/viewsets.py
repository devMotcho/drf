from rest_framework import mixins, viewsets

from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    get -> list -> Queryset
    get -> retrive -> Product Instance Detail view
    post -> create -> New Instance
    put -> Update
    path -> Partial Update
    delete -> destroy
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' # default

class ProductGenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    """
    get -> list -> Queryset
    get -> retrive -> Product Instance Detail view
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' # default