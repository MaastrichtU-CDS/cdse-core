

class AuthProviderUtils:

    @staticmethod
    def check_role_exist(roles: [str], claims) -> bool:
        for role in roles:
            if role in claims.get('realm_access').get('roles', []):
                return True

        return False
