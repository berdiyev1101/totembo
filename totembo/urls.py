from django.urls import path
from totembo.views import *
urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("signout/", signout, name="signout"),
    path("products/", GetProducts.as_view(), name="product"),
    path("category/<int:pk>/", Product_By_Catagory.as_view(), name="category")
]