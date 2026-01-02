from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class AgeGroup(models.Model):
    """Age groups for baby products"""

    name = models.CharField(max_length=50, unique=True)
    min_months = models.PositiveIntegerField(help_text="Minimum age in months")
    max_months = models.PositiveIntegerField(help_text="Maximum age in months")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["min_months"]
        verbose_name_plural = "Age Groups"

    def __str__(self):
        return f"{self.name} ({self.min_months}-{self.max_months} months)"


class SafetyCertification(models.Model):
    """Safety certifications for baby products"""

    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=20)
    description = models.TextField()
    icon = models.ImageField(upload_to="certifications/", blank=True, null=True)
    is_required = models.BooleanField(
        default=False, help_text="Is this certification required for sales?"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Category(models.Model):
    """Product categories for baby goods"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:category", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Main product model for baby goods"""

    GENDER_CHOICES = [
        ("U", "Unisex"),
        ("M", "Male"),
        ("F", "Female"),
    ]

    CONDITION_CHOICES = [
        ("NEW", "Brand New"),
        ("LIKE_NEW", "Like New"),
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    # Inventory
    sku = models.CharField(max_length=100, unique=True, help_text="Stock Keeping Unit")
    track_inventory = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    allow_backorder = models.BooleanField(default=False)

    # Product attributes
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    age_groups = models.ManyToManyField(AgeGroup, related_name="products")
    safety_certifications = models.ManyToManyField(
        SafetyCertification, blank=True, related_name="products"
    )

    # Baby-specific attributes
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="U")
    materials = models.TextField(
        help_text="List of materials (e.g., '100% Organic Cotton, BPA-free plastic')"
    )
    care_instructions = models.TextField(blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True)

    # Media
    featured_image = models.ImageField(
        upload_to="products/featured/", blank=True, null=True
    )

    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES, default="NEW"
    )

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.stock > 0 or self.allow_backorder

    @property
    def is_low_stock(self):
        return self.stock <= self.low_stock_threshold and self.stock > 0

    @property
    def discount_percentage(self):
        if self.compare_at_price and self.compare_at_price > self.price:
            return round(
                (self.compare_at_price - self.price) / self.compare_at_price * 100
            )
        return 0

    def get_safety_status(self):
        """Check if product has required safety certifications"""
        required_certs = SafetyCertification.objects.filter(is_required=True)
        product_certs = self.safety_certifications.all()

        if required_certs.count() == 0:
            return "complete"
        elif (
            required_certs.filter(id__in=product_certs).count()
            == required_certs.count()
        ):
            return "complete"
        else:
            return "incomplete"


class ProductVariant(models.Model):
    """Product variants for size, color, etc."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )

    name = models.CharField(max_length=100, help_text="e.g., 'Blue / 6-9 months'")
    sku = models.CharField(max_length=100, unique=True)

    # Variant-specific attributes
    size = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    pattern = models.CharField(max_length=100, blank=True)

    # Pricing override
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Inventory
    stock = models.PositiveIntegerField(default=0)
    track_inventory = models.BooleanField(default=True)

    # Image
    image = models.ImageField(upload_to="products/variants/", blank=True, null=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    @property
    def effective_price(self):
        return self.price if self.price else self.product.price

    @property
    def is_in_stock(self):
        return self.stock > 0 or self.product.allow_backorder


class ProductImage(models.Model):
    """Product gallery images"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.product.name} - Image {self.sort_order}"


class ProductReview(models.Model):
    """Customer reviews for products"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )  # 1-5 stars
    title = models.CharField(max_length=100)
    content = models.TextField()
    verified_purchase = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["product", "user"]

    def __str__(self):
        return f"{self.product.name} - {self.user.username} Review"
