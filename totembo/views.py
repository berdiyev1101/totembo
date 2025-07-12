from itertools import product
from venv import create

from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from django.db import models
from totembo.forms import SignUpForm, SignInForm
from totembo.models import Category, Product, Vendor, Contact, Like, Basket


# class Index(ListView):
#     template_name = "totembo/index.html"

class Index(ListView):
    model = Category
    template_name = "totembo/index.html"
    context_object_name = "data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['quartz_products'] = Product.objects.all()[:4]
        context['automatic_products'] = Product.objects.all()[4:8]
        context['vendors'] = Vendor.objects.all()
        context['chains'] = Product.objects.all()[8:12]

        return context

class ProductDetail(DetailView):
    model = Product
    template_name = "totembo/detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(pk=self.kwargs['pk'])
        products = Product.objects.all()
        data = []
        i = 0
        while i <= 5:
            from random import randint
            random_product = products[randint(0,len(products)-1)]
            if not random_product in data:
                data.append(random_product)
                i += 1
        context['products'] = data
        return context

def signup(request):
    form = SignUpForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect("index")
    context = {
        "title":"Sign Up",
        "form":form
    }
    return render(request,"totembo/signup.html",context)


def signin(request):
    form = SignInForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect("index")
    context = {
        "title":"Sign In",
        "form":form
    }
    return render(request,"totembo/signin.html",context)

def signout(request):
    logout(request)
    return redirect("signin")

class GetProducts(ListView):
    model = Product
    context_object_name = "products"
    template_name ="totembo/index.html"

    def get_queryset(self):
        return Product.objects.all()



class Product_By_Catagory(ListView):
    model = Product
    context_object_name = "products"
    template_name = "totembo/category_detail.html"
    paginate_by = 12

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        products = Product.objects.filter(category=category)
        sort_field = self.request.GET.get("sort")
        price_field = self.request.GET.getlist("price")
        color_field = self.request.GET.getlist("color")
        if sort_field:
            products = products.order_by(sort_field)
        if price_field:
            price_choices = {
                '0-100':(0,100),
                '100-200':(100,200),
                '200-300':(200,300),
                '300-400':(300,400),
            }
            price_list = [price_choices[price] for price in price_field if price in price_choices]
            if price_list:
                products = products.filter(
                    price__gte=min(price[0] for price in price_list),
                    price__lte=max(price[1] for price in price_list)
                )

        if color_field:
            products = products.filter(color__in=color_field)

        return products

def contact(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        Contact.objects.create(full_name=full_name, email=email, subject=subject, message=message)

    context = {
        "title":"Contact"
    }
    return render(request, "totembo/contact.html", context)



class LikeList(ListView):
    model = Like
    template_name = "totembo/like.html"
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user
        likes = Like.objects.filter(user=user)
        products = [like.product for like in likes]
        return products

def user_like(request, pk):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(pk=pk)
    if user:
        user_products = Like.objects.filter(user=user)
        if product in [like.product for like in user_products]:
            product_like = Like.objects.filter(user=user, product=product)
            product_like.delete()
        else:
            Like.objects.create(user=user, product=product)
    next_page = request.META.get("HTTP_REFERER","index")
    return redirect(next_page)


def basket(request):
    basket_products = Basket.objects.filter(user=request.user)
    context = {
        "title":"Basket",
        "products":basket_products
    }
    return render(request,"totembo/basket.html", context)

def basket_add(request,pk):
    product = get_object_or_404(Basket,pk=pk)
    basket_product, created = Basket.objects.get_or_create(product=product, user=request.user)
    if not created:
        basket_product.quantity += 1
        basket_product.save()
    next_page = request.META.get("HTTP_REFERER","index")
    return redirect(next_page)

def basket_update(request,pk):
    product = get_object_or_404(Basket, user=request.user, pk=pk)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity",1))
        if quantity > 0:
            product.quantity = quantity
            product.save()
        else:
            product.delete()
        return redirect("basket")

def basket_remove(request,pk):
    product = get_object_or_404(Basket,user=request.user, pk=pk)
    product.delete()
    return redirect("basket")








