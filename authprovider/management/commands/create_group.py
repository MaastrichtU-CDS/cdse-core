from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from authprovider.models import RolesAndPermissions
import logging

class Command(BaseCommand):
    help = "Creates default permission groups for users"

    def handle(self, *args, **options):

        for group_name in RolesAndPermissions.GROUPS:

            new_group, created = Group.objects.get_or_create(name=group_name)
            print(group_name, "group already exists:", not created)

            # Loop models in group
            if created is True:
                for app_model in RolesAndPermissions.GROUPS[group_name]:
                    # Loop permissions in group/model
                    for permission_name in RolesAndPermissions.GROUPS[group_name][app_model]:

                        # Generate permission name as Django would generate it
                        name = "Can {} {}".format(permission_name, app_model)
                        print("Creating {}".format(name))

                        try:
                            model_add_perm = Permission.objects.get(name=name)
                        except Permission.DoesNotExist:
                            logging.warning("Permission not found with name '{}'.".format(name))
                            continue

                        new_group.permissions.add(model_add_perm)
