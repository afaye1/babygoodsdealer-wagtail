from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.search import index
from django.db import models
from django.utils.text import slugify
from products.models import Product, Category


# Custom StreamField blocks for baby products
class ProductBlock(blocks.StructBlock):
    """Product block to feature specific baby products"""

    product = blocks.ChoiceBlock(
        choices=[],  # Will be populated dynamically
        label="Select Product",
    )
    show_description = blocks.BooleanBlock(default=True, required=False)
    show_price = blocks.BooleanBlock(default=True, required=False)

    class Meta:
        icon = "tag"
        template = "blocks/product_block.html"


class BabyTipsBlock(blocks.StructBlock):
    """Block for baby care tips and safety guides"""

    title = blocks.CharBlock(max_length=100)
    content = RichTextField()
    age_groups = blocks.MultipleChoiceBlock(
        choices=[
            ("newborn", "Newborn (0-2 months)"),
            ("infant", "Infant (3-11 months)"),
            ("toddler", "Toddler (1-3 years)"),
        ],
        required=False,
    )
    featured_image = ImageChooserBlock(required=False)

    class Meta:
        icon = "help"
        template = "blocks/baby_tips_block.html"


class SafetyGuideBlock(blocks.StructBlock):
    """Block for safety guides and certification information"""

    title = blocks.CharBlock(max_length=100)
    safety_standard = blocks.CharBlock(max_length=100, help_text="e.g., 'ASTM F963-17'")
    key_points = blocks.ListBlock(
        blocks.CharBlock(max_length=200), help_text="Key safety points for parents"
    )
    warning_text = blocks.TextBlock(
        required=False, help_text="Any warnings or precautions"
    )

    class Meta:
        icon = "warning"
        template = "blocks/safety_guide_block.html"


class AgeBasedProductBlock(blocks.StructBlock):
    """Block to show products for specific age groups"""

    age_group_title = blocks.CharBlock(max_length=100)
    age_range = blocks.CharBlock(max_length=50, help_text="e.g., '6-12 months'")
    products = blocks.ListBlock(
        ProductBlock(), help_text="Select products suitable for this age group"
    )
    custom_message = blocks.TextBlock(required=False)

    class Meta:
        icon = "group"
        template = "blocks/age_based_products.html"


# Main content page models
class HomePage(Page):
    """Home page with featured products and baby guides"""

    hero_title = models.CharField(max_length=200, default="Premium Baby Products")
    hero_subtitle = models.TextField(
        default="Safe, organic, and certified products for your little ones"
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    featured_products = StreamField(
        [
            ("featured_products", blocks.ListBlock(ProductBlock())),
            ("baby_tips", BabyTipsBlock()),
            ("safety_guide", SafetyGuideBlock()),
            ("age_products", AgeBasedProductBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("featured_products"),
    ]

    class Meta:
        verbose_name = "Home Page"


class ProductCategoryPage(Page):
    """Page for product categories"""

    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="page"
    )

    intro_text = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    safety_info = StreamField(
        [
            ("safety_guide", SafetyGuideBlock()),
            ("baby_tips", BabyTipsBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("intro_text"),
        FieldPanel("featured_image"),
        FieldPanel("safety_info"),
    ]

    class Meta:
        verbose_name = "Product Category Page"


class ProductDetailPage(Page):
    """Detailed product page with Wagtail integration"""

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="page"
    )

    additional_content = StreamField(
        [
            ("safety_info", SafetyGuideBlock()),
            ("baby_tips", BabyTipsBlock()),
            ("age_recommendations", AgeBasedProductBlock()),
            ("related_content", blocks.RichTextBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    care_instructions = RichTextField(blank=True)
    safety_warnings = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("product"),
        FieldPanel("care_instructions"),
        FieldPanel("safety_warnings"),
        FieldPanel("additional_content"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("care_instructions"),
        index.SearchField("safety_warnings"),
    ]

    class Meta:
        verbose_name = "Product Detail Page"


class SafetyGuidePage(Page):
    """Page for comprehensive safety guides"""

    target_age_group = models.CharField(
        max_length=100, help_text="e.g., 'Newborns', 'Infants 6-12 months'"
    )
    safety_standards = RichTextField()
    key_guidelines = StreamField(
        [
            ("safety_guide", SafetyGuideBlock()),
            ("baby_tips", BabyTipsBlock()),
        ],
        use_json_field=True,
    )

    featured_products = models.ManyToManyField(
        Product, blank=True, related_name="safety_guides"
    )

    content_panels = Page.content_panels + [
        FieldPanel("target_age_group"),
        FieldPanel("safety_standards"),
        FieldPanel("key_guidelines"),
        FieldPanel("featured_products"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("target_age_group"),
        index.SearchField("safety_standards"),
    ]

    class Meta:
        verbose_name = "Safety Guide Page"


class BlogPage(Page):
    """Blog for parenting tips and baby care advice"""

    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    author = models.CharField(max_length=100)
    reading_time = models.PositiveIntegerField(
        help_text="Estimated reading time in minutes"
    )

    content = StreamField(
        [
            ("content", blocks.RichTextBlock()),
            ("baby_tips", BabyTipsBlock()),
            ("safety_guide", SafetyGuideBlock()),
            ("age_products", AgeBasedProductBlock()),
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True,
    )

    tags = models.CharField(max_length=200, help_text="Comma-separated tags")

    content_panels = Page.content_panels + [
        FieldPanel("featured_image"),
        FieldPanel("author"),
        FieldPanel("reading_time"),
        FieldPanel("content"),
        FieldPanel("tags"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("content"),
        index.SearchField("tags"),
    ]

    class Meta:
        verbose_name = "Blog Post"


# Inline model for product recommendations
class ProductRecommendation(models.Model):
    """Product recommendations within pages"""

    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="product_recommendations"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reason = models.CharField(
        max_length=200, help_text="Why this product is recommended"
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.page.title} - {self.product.name}"
