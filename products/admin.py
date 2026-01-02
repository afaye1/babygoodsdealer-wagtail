from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    AgeGroup,
    SafetyCertification,
    Category,
    Product,
    ProductVariant,
    ProductImage,
    ProductReview,
)


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "age_range", "description"]
    list_filter = ["min_months", "max_months"]
    search_fields = ["name", "description"]

    def age_range(self, obj):
        return f"{obj.min_months}-{obj.max_months} months"


@admin.register(SafetyCertification)
class SafetyCertificationAdmin(admin.ModelAdmin):
    list_display = ["name", "abbreviation", "icon_preview", "is_required"]
    list_filter = ["is_required"]
    search_fields = ["name", "abbreviation"]

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return "No icon"

    icon_preview.short_description = "Icon"


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ["name", "sku", "size", "color", "price", "stock", "is_active"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ["image", "alt_text", "sort_order"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "image_preview", "product_count", "is_active"]
    list_filter = ["is_active", "parent"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"

    image_preview.short_description = "Image"

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price",
        "stock_status",
        "age_groups_display",
        "safety_status",
        "is_active",
    ]
    list_filter = [
        "category",
        "gender",
        "condition",
        "is_active",
        "is_featured",
        "age_groups",
        "safety_certifications",
    ]
    search_fields = ["name", "description", "sku"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["age_groups", "safety_certifications"]
    inlines = [ProductVariantInline, ProductImageInline]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "description",
                    "short_description",
                )
            },
        ),
        ("Pricing", {"fields": ("price", "compare_at_price", "cost_price")}),
        (
            "Inventory",
            {
                "fields": (
                    "sku",
                    "track_inventory",
                    "stock",
                    "low_stock_threshold",
                    "allow_backorder",
                )
            },
        ),
        (
            "Baby Product Attributes",
            {
                "fields": (
                    "age_groups",
                    "gender",
                    "materials",
                    "care_instructions",
                    "country_of_origin",
                )
            },
        ),
        ("Safety", {"fields": ("safety_certifications",)}),
        ("Media", {"fields": ("featured_image",)}),
        (
            "Status & SEO",
            {
                "fields": (
                    "is_active",
                    "is_featured",
                    "condition",
                    "meta_title",
                    "meta_description",
                )
            },
        ),
    )

    def stock_status(self, obj):
        if not obj.track_inventory:
            return "Not Tracked"
        elif obj.allow_backorder:
            return format_html('<span style="color: blue;">Backorder OK</span>')
        elif obj.stock > obj.low_stock_threshold:
            return format_html(
                '<span style="color: green;">In Stock ({})</span>', obj.stock
            )
        elif obj.stock > 0:
            return format_html(
                '<span style="color: orange;">Low Stock ({})</span>', obj.stock
            )
        else:
            return format_html('<span style="color: red;">Out of Stock</span>')

    stock_status.short_description = "Stock Status"

    def age_groups_display(self, obj):
        groups = list(obj.age_groups.values_list("name", flat=True))
        return ", ".join(groups[:3]) + ("..." if len(groups) > 3 else "")

    age_groups_display.short_description = "Age Groups"

    def safety_status(self, obj):
        status = obj.get_safety_status()
        if status == "complete":
            return format_html('<span style="color: green;">✅ Safe</span>')
        else:
            return format_html('<span style="color: red;">⚠️ Incomplete</span>')

    safety_status.short_description = "Safety Status"


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "size", "color", "price", "stock", "is_active"]
    list_filter = ["size", "color", "is_active", "product__category"]
    search_fields = ["name", "sku", "product__name"]

    def price(self, obj):
        return f"${obj.effective_price}"

    def stock(self, obj):
        if obj.is_in_stock:
            return f"{obj.stock} units"
        return "Out of stock"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image_preview", "alt_text", "sort_order"]
    list_filter = ["product__category"]
    search_fields = ["product__name", "alt_text"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" />', obj.image.url)
        return "No image"

    image_preview.short_description = "Image"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "user",
        "rating_display",
        "title",
        "is_approved",
        "created_at",
    ]
    list_filter = ["rating", "is_approved", "verified_purchase", "product__category"]
    search_fields = ["product__name", "user__username", "title", "content"]
    actions = ["approve_reviews", "reject_reviews"]

    def rating_display(self, obj):
        stars = "⭐" * obj.rating
        return f"{stars} ({obj.rating}/5)"

    rating_display.short_description = "Rating"

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    approve_reviews.short_description = "Approve selected reviews"

    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)

    reject_reviews.short_description = "Reject selected reviews"
