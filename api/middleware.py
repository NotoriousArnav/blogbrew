import logging
from urllib.parse import urlparse

from django.conf import settings as s

log = logging.getLogger(__name__)

LOCALHOST_DOMAINS = set([
    "localhost", "127.0.0.1", "0.0.0.0", "[::1]",
])

class CrossOriginAccessControlMiddleware(object):
    """ Middleware to set HTTP Access-Control-* headers.

        Example ``settings.py`` settings::

            # Should any 'localhost' origin be allowed? Useful during
            # development. Default: False
            CROSS_ORIGIN_ALLOW_LOCALHOST = DEBUG
            # The origins which should be allowed, by exact match.
            # Default: []

            CROSS_ORIGIN_ALLOWED_ORIGINS = set([
                "http://example.com
            ])

            # Should credentials (cookies, HTTP auth) should be allowed from
            # allowed origins?
            CROSS_ORIGIN_ALLOW_CREDENTIALS = True

            # The methods which should be allowed.
            # Default: []
            CROSS_ORIGIN_ALLOWED_METHODS = set([
                "GET", "POST", "PUT", "DELETE", "OPTIONS",
            ])

            # The headers which should be allowed.
            # Default: []
            CROSS_ORIGIN_ALLOWED_HEADERS = set([])

            # A value for Access-Control-Max-Age. Note: only set if
            # Access-Control-Allow-Methods or Access-Control-Allow-Headers is
            # also being set.
            # Default: None
            CROSS_ORIGIN_MAX_AGE = 60 * 60 * 48

        See also: https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS
    """

    def process_request(self, request):
        origin = request.META.get("HTTP_ORIGIN")
        if origin is None:
            return
        if not self.origin_allowed(origin):
            log.warning(
                "Origin %r not allowed! (see CROSS_ORIGIN_ALLOWED_ORIGINS and "
                "CROSS_ORIGIN_ALLOW_LOCALHOST)!", origin
            )
            return

        headers = getattr(request, "cross_origin_headers", {})
        headers.update({
            "Access-Control-Allow-Origin": origin,
        })

        if getattr(s, "CROSS_ORIGIN_ALLOW_CREDENTIALS", True):
            headers.update({
                "Access-Control-Allow-Credentials": "true"
            })

        request_method = request.META.get("HTTP_ACCESS_CONTROL_REQUEST_METHOD")
        if request_method is not None:
            if request_method in getattr(s, "CROSS_ORIGIN_ALLOWED_METHODS", []):
                headers.update({
                    "Access-Control-Allow-Methods": request_method,
                })
            else:
                log.warning("Requested method %r not allowed! "
                            "(see CROSS_ORIGIN_ALLOWED_METHODS)",
                            request_method)

        request_headers = request.META.get("HTTP_ACCESS_CONTROL_ALLOW_HEADERS")
        if request_headers is not None:
            allowed_headers = getattr(s, "CROSS_ORIGIN_ALLOWED_HEADERS", [])
            request_headers = [h.strip() for h in request_headers.split(",")]
            return_headers = [h for h in request_headers if h in allowed_headers]
            if len(return_headers) != len(request_headers):
                log.warning("Requested header(s) %r not allowed! "
                            "(see CROSS_ORIGIN_ALLOWED_HEADERS)",
                            set(request_headers) - set(allowed_headers))
            headers.update({
                "Access-Control-Allow-Headers": ", ".join(return_headers),
            })

        max_age = getattr(s, "CROSS_ORIGIN_MAX_AGE", None)
        if max_age is not None and (request_method or request_headers):
            headers.update({
                "Access-Control-Max-Age": max_age,
            })

        request.cross_origin_headers = headers

    def origin_allowed(self, origin):
        allowed_origins = getattr(s, "CROSS_ORIGIN_ALLOWED_ORIGINS", [])
        if origin in allowed_origins:
            return True
        if getattr(s, "CROSS_ORIGIN_ALLOW_LOCALHOST", False):
            domain, _, _ = urlparse(origin).netloc.rpartition(":")
            return domain in LOCALHOST_DOMAINS
        return False

    def process_response(self, request, response):
        cross_origin_headers = getattr(request, "cross_origin_headers", None)
        if cross_origin_headers is not None:
            for name, value in cross_origin_headers.items():
                response[name] = value
        return response
