from django.utils import timezone

from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.http import HttpRequest


def get_current_year() -> int:
    return timezone.now().year


def get_safe_next_url(request: HttpRequest, fallback_url_name: str) -> str:
    """
    Gets a safe 'next' URL from the request's GET parameters,
    or returns a fallback URL.

    Args:
        request: The Django request object.
        fallback_url_name: The name of the URL pattern to use as a fallback.

    Returns:
        A safe URL for redirection.
    """
    
    next_url = request.GET.get('next')
    
    if (
        next_url and
        url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
    ):
        return next_url
    
    # If not safe or doesn't exist, return fallback
    return reverse(fallback_url_name)