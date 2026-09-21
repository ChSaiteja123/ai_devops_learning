"""
Audit Middleware.

HOW DJANGO MIDDLEWARE WORKS:
-----------------------------
Middleware wraps every request/response cycle.

Request  → Middleware1 → Middleware2 → ... → View
Response ← Middleware1 ← Middleware2 ← ... ← View

Each middleware's __call__ method:
  1. Receives the request
  2. Optionally modifies it
  3. Calls get_response(request) to pass it down the chain
  4. Receives the response
  5. Optionally modifies it
  6. Returns the response

WHAT WE AUDIT:
--------------
We record every mutating request (POST/PUT/PATCH/DELETE) and
login/logout actions. GET requests to API endpoints are recorded
at DEBUG level for full auditability (optional).

SENSITIVE FIELDS are stripped from request_data before storage.
"""
import json
import logging
from .models import AuditLog

logger = logging.getLogger(__name__)

# Fields that must never be stored in audit logs
SENSITIVE_FIELDS = {
    'password', 'password1', 'password2', 'new_password', 'old_password',
    'token', 'access', 'refresh', 'secret', 'api_key', 'credit_card',
    'cvv', 'ssn',
}

# HTTP methods that mutate state — always audit these
AUDITED_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}

# URL paths that are never audited (too noisy or irrelevant)
EXCLUDED_PATHS = {'/health/', '/metrics/', '/static/', '/media/', '/__debug__/'}


def _get_client_ip(request) -> str:
    """Extract real client IP, handling reverse proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def _sanitize(data: dict) -> dict:
    """Remove sensitive fields from a dict (one level deep)."""
    if not isinstance(data, dict):
        return {}
    return {
        k: '***REDACTED***' if k.lower() in SENSITIVE_FIELDS else v
        for k, v in data.items()
    }


def _parse_request_data(request) -> dict:
    """Safely parse request body as JSON or form data."""
    try:
        if request.content_type and 'application/json' in request.content_type:
            body = request.body
            if body:
                return _sanitize(json.loads(body))
    except Exception:
        pass
    try:
        return _sanitize(dict(request.POST))
    except Exception:
        return {}


class AuditMiddleware:
    """
    Records mutating API requests to the AuditLog model.
    Runs after the response is returned so it never blocks the request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request normally first
        response = self.get_response(request)

        # Decide whether to audit this request
        try:
            self._maybe_audit(request, response)
        except Exception as exc:
            # Audit logging must NEVER crash the application
            logger.error('AuditMiddleware error: %s', exc, exc_info=True)

        return response

    def _maybe_audit(self, request, response):
        path = request.path

        # Skip excluded paths
        if any(path.startswith(p) for p in EXCLUDED_PATHS):
            return

        # Only audit API paths and auth endpoints
        if not (path.startswith('/api/') or path.startswith('/accounts/')):
            return

        # Only audit mutating methods for non-login paths
        method = request.method.upper()
        is_login = path.endswith('/login/') or path.endswith('/token/')
        if method not in AUDITED_METHODS and not is_login:
            return

        # Determine action
        action = self._resolve_action(method, path, response.status_code)
        if not action:
            return

        # Resolve user
        user = None
        username_snapshot = 'anonymous'
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
            username_snapshot = request.user.username

        # Extract resource info from path  e.g. /api/v1/courses/5/
        resource_type, resource_id = self._parse_resource(path)

        AuditLog.objects.create(
            user=user,
            username_snapshot=username_snapshot,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            method=method,
            path=path,
            ip_address=_get_client_ip(request) or None,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            status_code=response.status_code,
            request_data=_parse_request_data(request),
        )

    def _resolve_action(self, method: str, path: str, status_code: int) -> str | None:
        """Map HTTP method + path to audit action string."""
        if path.endswith('/login/') or path.endswith('/token/'):
            if status_code < 300:
                return 'LOGIN'
            return 'FAILED_LOGIN'
        if path.endswith('/logout/'):
            return 'LOGOUT'
        if 'change-password' in path:
            return 'PASSWORD_CHANGE'
        mapping = {
            'POST':   'CREATE',
            'PUT':    'UPDATE',
            'PATCH':  'UPDATE',
            'DELETE': 'DELETE',
        }
        return mapping.get(method)

    def _parse_resource(self, path: str):
        """
        Extract resource_type and resource_id from URL path.
        e.g. /api/v1/courses/5/lessons/ → ('courses', '5')
        """
        parts = [p for p in path.strip('/').split('/') if p]
        # parts: ['api', 'v1', 'courses', '5', ...]
        if len(parts) >= 3 and parts[0] == 'api':
            resource_type = parts[2] if len(parts) > 2 else ''
            resource_id = parts[3] if len(parts) > 3 and parts[3].isdigit() else ''
            return resource_type, resource_id
        return '', ''
