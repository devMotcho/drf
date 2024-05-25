from django.urls import path

from .views import (
    ProductDetailAPIView,
    ProductUpdateAPIView,
    ProductDestroyAPIView,
    ProductListCreateAPIView,
)

urlpatterns = [
    path('', ProductListCreateAPIView.as_view()),
    path('<int:pk>/update/', ProductUpdateAPIView.as_view()),
    path('<int:pk>/delete/', ProductDestroyAPIView.as_view()),
    path('<int:pk>/', ProductDetailAPIView.as_view()),
]