from django.urls import path

from .views import (
    ProductDetailAPIView,
    ProductUpdateAPIView,
    ProductDestroyAPIView,
    ProductListCreateAPIView,
    ProductMixinView,
)

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='product-list'),
    path('<int:pk>/update/', ProductUpdateAPIView.as_view(), name='product-edit'),
    path('<int:pk>/delete/', ProductDestroyAPIView.as_view()),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
]