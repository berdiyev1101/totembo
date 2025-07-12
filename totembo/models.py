from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models



# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None,**kwargs):
        if not email:
            raise ValueError("Email must be fill ")
        email = self.normalize_email(email=email)
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be is_staff TRUE")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be is_superuser TRUE")
        return self.create_user(email=email, password=password, **kwargs)


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    zipcode = models.CharField(max_length=250, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Category(models.Model):
    title = models.CharField(max_length=50,)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"



class Product(models.Model):
    COLOR_CHOICES = [
        ("gold","gold"),
        ("yellow", "yellow"),
        ("black", "black"),
        ("silver", "silver")
    ]
    TYPE_CHOICES = [
        ("quartz edition","quartz edition"),
        ("chain edition","chain edition"),
        ("automatic edition","automatic edition"),
    ]
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/")
    price = models.CharField(max_length=15)
    info = models.TextField(max_length=200)
    color = models.CharField(max_length=30, choices=COLOR_CHOICES, default="gold")
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="quartz edition" )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_image(self):
            return self.image.url


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Vendor(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title


class Gallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="images/")

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.full_name

class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title} ------->> {self.user.email}"


class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return self.user.email

    def get_total_price(self):
        return self.product.price * self.quantity
