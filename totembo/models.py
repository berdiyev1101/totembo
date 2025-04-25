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

