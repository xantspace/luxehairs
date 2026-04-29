from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(
        max_length=100, help_text="e.g. Virgin Cambodian, Brazilian Gold")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, help_text="If set, shows as strikethrough")
    image = models.ImageField(upload_to='products/')
    video = models.FileField(
        upload_to='products/videos/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)

    # badges
    badge_text = models.CharField(
        max_length=50, blank=True, help_text="e.g. New Edition, Elite, Top")

    is_new = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    points = models.IntegerField(default=0)
    # e.g. Member, Elite, Gold
    tier = models.CharField(max_length=20, default='Member')
    profile_image = models.FileField(
        upload_to='profiles/', blank=True, null=True)

    # Personal & Aesthetic
    birth_date = models.DateField(null=True, blank=True)
    face_shape = models.CharField(max_length=50, blank=True, default='Oval')
    lustre_bias = models.CharField(
        max_length=50, blank=True, default='Natural High Shine')

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    reference_id = models.CharField(max_length=20, unique=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.reference_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    # Snapshot of price at purchase
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name if self.product else 'Unknown'}"

# --- Cart System ---


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
