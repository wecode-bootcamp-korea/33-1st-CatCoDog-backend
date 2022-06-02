from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('products', include('products.urls')),
]