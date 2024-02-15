from django.urls import path
from Product_Details import views

urlpatterns = [
    path('product',views.Product_API.as_view()),
    path('product/<int:pk>', views.Product_API.as_view()),
    path('data', views.Data_presentation.as_view()),
]