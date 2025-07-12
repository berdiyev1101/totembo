from django.urls import path
from totembo.views import *
urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("signout/", signout, name="signout"),
    path("contact/", contact, name="contact"),
    path("likes/", LikeList.as_view(), name="likes"),
    path("products/", GetProducts.as_view(), name="product"),
    path("category/<int:pk>/", Product_By_Catagory.as_view(), name="category"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="detail"),
    path("basket_update/<int:pk>/", basket_update, name="basket_update"),
    path("basket_remove/<int:pk>/", basket_remove, name="basket_remove"),
    path("basket_add/<int:pk>/", basket_add, name="basket_add"),
    path("likes/<int:pk>/", user_like, name="like"),
    path("basket/", basket, name="basket")
]