# context_processors.py
from typing import Any

from .models import SEOPage


def seo_metadata(request) -> dict[str, Any]:
    current_path = request.path

    try:
        page = SEOPage.objects.get(page_type=current_path)
        return {"global_seo_meta": page.as_meta(request)}
    except SEOPage.DoesNotExist:
        pass

    return {"global_seo_meta": None}
