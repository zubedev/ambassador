from logging import getLogger

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

logger = getLogger(__name__)


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """User Manager overridden from BaseUserManager for User"""

    def _create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        if not email:  # check for an empty email
            logger.error("User must set an email address")
            raise AttributeError("User must set an email address")
        else:  # normalizes the provided email
            email = self.normalize_email(email)
            logger.debug(f"Normalized email: {email}")

        # create user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes/encrypts password
        user.save(using=self._db)  # safe for multiple databases
        logger.debug(f"User created: {user}")
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_ambassador', False)
        logger.debug(f"Creating user: email={email}, "
                     f"extra_fields={extra_fields}")
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password=None, **extra_fields):
        """Creates and returns a new staffuser using an email address"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_ambassador', False)
        logger.debug(f"Creating staffuser: email={email}, "
                     f"extra_fields={extra_fields}")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a new superuser using an email address"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_ambassador', False)
        logger.debug(f"Creating superuser: email={email}, "
                     f"extra_fields={extra_fields}")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Extended User model"""
    username = None  # disable username field
    email = models.EmailField(unique=True)
    is_ambassador = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def revenue(self):
        orders = self.order_set.filter(is_complete=True)
        if self.is_ambassador:
            return sum(o.ambassador_revenue for o in orders)
        else:  # admin
            return sum(o.admin_revenue for o in orders)


class Product(TimeStampedModel):
    """Product model"""
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=254)
    image = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class Link(TimeStampedModel):
    """Product and User model Link"""
    code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.code


class Order(TimeStampedModel):
    """Order model"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    trans_id = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    amb_email = models.EmailField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=254, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    zip = models.CharField(max_length=15, null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    @property
    def admin_revenue(self):
        items = self.order_items.all()
        return sum(i.admin_revenue for i in items)

    @property
    def ambassador_revenue(self):
        items = self.order_items.all()
        return sum(i.ambassador_revenue for i in items)


class OrderItem(TimeStampedModel):
    """Order Item model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    admin_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    ambassador_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
