"""Custom context processor
"""

from django.conf import settings


def domain_context_processor(request):
    """domain_context_processor
    Args:
        request:

    Returns:
    """

    return {
        "DISPLAY_NIST_HEADERS": (
            settings.DISPLAY_NIST_HEADERS
            if hasattr(settings, "DISPLAY_NIST_HEADERS")
            else True
        ),
    }
