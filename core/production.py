from core.settings import *
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
DEBUG = int(os.environ.get("DEBUG", default=0))


DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "SQL_ENGINE", "django.db.backends.sqlite3"), "NAME": os.environ.get(
                "SQL_DATABASE_DJANGO", os.path.join(
                    BASE_DIR, "db.sqlite3")), "USER": os.environ.get(
                        "SQL_USER_DJANGO", "user"), "PASSWORD": os.environ.get(
                            "SQL_PASSWORD_DJANGO", "password"), "HOST": os.environ.get(
                                "SQL_HOST", "localhost"), "PORT": os.environ.get(
                                    "SQL_PORT", "5432"), }}

OIDC_OP_LOGOUT_ENDPOINT = os.environ.get("OIDC_OP_LOGOUT_ENDPOINT", "")
LOGOUT_REDIRECT_URL = os.environ.get("LOGOUT_REDIRECT_URL", "")
OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ.get(
    "OIDC_OP_AUTHORIZATION_ENDPOINT", "")
OIDC_OP_TOKEN_ENDPOINT = os.environ.get("OIDC_OP_TOKEN_ENDPOINT", "")
OIDC_OP_USER_ENDPOINT = os.environ.get("OIDC_OP_USER_ENDPOINT", "")
OIDC_OP_JWKS_ENDPOINT = os.environ.get("OIDC_OP_JWKS_ENDPOINT", "")
OIDC_RP_CLIENT_ID = os.environ.get("OIDC_RP_CLIENT_ID", "")
OIDC_RP_CLIENT_SECRET = os.environ.get("OIDC_RP_CLIENT_SECRET", "")
OIDC_RP_SIGN_ALGO = os.environ.get("OIDC_RP_SIGN_ALGO", "")
OIDC_RP_SCOPES = os.environ.get("OIDC_RP_SCOPES", "")
OIDC_OP_LOGOUT_URL_METHOD = os.environ.get("OIDC_OP_LOGOUT_URL_METHOD", "")
