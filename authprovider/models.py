from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from .utils import AuthProviderUtils


def default_user_settings(user, claims):
    user.first_name = claims.get('given_name', '')
    user.last_name = claims.get('family_name', '')
    user.is_superuser = AuthProviderUtils.check_role_exist(['super_admin'], claims)
    user.is_staff = AuthProviderUtils.check_role_exist(['it_administrator', 'mdr_regulator', 'medical_professional',
                                                        'super_admin'], claims)
    return


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(CustomOIDCAuthenticationBackend, self).create_user(claims)

        default_user_settings(user, claims)
        user.save()

        return user

    def update_user(self, user, claims):
        default_user_settings(user, claims)
        user.save()

        return user
