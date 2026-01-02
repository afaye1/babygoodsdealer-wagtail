from wagtail.snippets.models import register_snippet
from products.models import AgeGroup, SafetyCertification


# Register snippets for Wagtail admin
@register_snippet
class AgeGroupSnippet:
    pass


@register_snippet
class SafetyCertificationSnippet:
    pass
