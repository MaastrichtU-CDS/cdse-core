from core.settings import *

# This will overwrite anything in settings.py
OIDC_OP_LOGOUT_ENDPOINT = (
    "http://localhost:8080/auth/realms/maastro/protocol/openid-connect/logout"
)
LOGOUT_REDIRECT_URL = "http://localhost:8000/"
OIDC_OP_AUTHORIZATION_ENDPOINT = (
    "http://localhost:8080/auth/realms/maastro/protocol/openid-connect/auth"
)
OIDC_OP_TOKEN_ENDPOINT = (
    "http://localhost:8080/auth/realms/maastro/protocol/openid-connect/token"
)
OIDC_OP_USER_ENDPOINT = (
    "http://localhost:8080/auth/realms/maastro/protocol/openid-connect/userinfo"
)
OIDC_OP_JWKS_ENDPOINT = (
    "http://localhost:8080/auth/realms/maastro/protocol/openid-connect/certs"
)
OIDC_RP_CLIENT_ID = "cdse-core"
OIDC_RP_CLIENT_SECRET = "5b5c41fd-9be0-41c6-a247-f504e4cf4c71"
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_SCOPES = "openid email roles profile"
OIDC_OP_LOGOUT_URL_METHOD = "authprovider.provider_logout"

AUTHENTICATION_BACKENDS = ("authprovider.models.CustomOIDCAuthenticationBackend",)

MIDDLEWARE = MIDDLEWARE + [
    "mozilla_django_oidc.middleware.SessionRefresh",
]
