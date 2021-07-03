import logging

from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from authprovider.utils import AuthProviderUtils
from django.contrib.auth.models import Group


class RolesAndPermissions:
    GROUPS = {
        "super_admin": {
            "log entry": ["add", "delete", "change", "view"],
            "group": ["add", "delete", "change", "view"],
            "permission": ["add", "delete", "change", "view"],
            "user": ["add", "delete", "change", "view"],
            "content type": ["add", "delete", "change", "view"],
            "session": ["add", "delete", "change", "view"],
            "datasource": ["add", "delete", "change", "view"],
            "predictionmodel": ["add", "delete", "change", "view"],
        },
        "it_administrator": {
            "predictionmodel": ["view"],
        },
        "mdr_regulator": {
            "predictionmodel": ["view"],
        },
        "medical_professional": {
            "predictionmodel": ["view"],
        },
    }


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(CustomOIDCAuthenticationBackend, self).create_user(claims)
        self.default_user_settings(user, claims)
        self.default_group_settings(user, claims)
        user.save()
        return user

    def update_user(self, user, claims):
        self.default_user_settings(user, claims)
        self.default_group_settings(user, claims)
        user.save()
        return user

    def verify_claims(self, claims):
        verified = super(CustomOIDCAuthenticationBackend, self).verify_claims(claims)
        has_required_role = AuthProviderUtils.check_role_exist_in_claim(
            list(RolesAndPermissions.GROUPS.keys()), claims
        )
        return verified and has_required_role

    @staticmethod
    def default_user_settings(user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.is_superuser = AuthProviderUtils.check_role_exist_in_claim(
            ["super_admin"], claims
        )
        user.is_staff = AuthProviderUtils.check_role_exist_in_claim(
            list(RolesAndPermissions.GROUPS.keys()), claims
        )
        return

    @staticmethod
    def default_group_settings(user, claims):
        for role in claims.get("realm_access").get("roles", []):
            if role in list(RolesAndPermissions.GROUPS.keys()):
                try:
                    existing_group = Group.objects.get(name=role)
                    existing_group.user_set.add(user)
                except Group.DoesNotExist:
                    logging.warning(
                        "Role from claim doesn't exist in groups, please run create_group command"
                    )
                    continue
