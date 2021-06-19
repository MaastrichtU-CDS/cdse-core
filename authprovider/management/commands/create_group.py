from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
import logging

GROUPS = {
    "it_administration": {
        "log entry": ["add", "delete", "change", "view"],
        "group": ["add", "delete", "change", "view"],
        "permission": ["add", "delete", "change", "view"],
        "user": ["add", "delete", "change", "view"],
        "content type": ["add", "delete", "change", "view"],
        "session": ["add", "delete", "change", "view"],

        "datasource": ["add", "delete", "change", "view"],
        "predictionmodel": ["add", "delete", "change", "view"],
    },

    "medical_staff": {
        "predictionmodel": ["view"],
    },
}


class Command(BaseCommand):
    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):

        for group_name in GROUPS:

            new_group, created = Group.objects.get_or_create(name=group_name)
            print(group_name, "group already exists:", not created)

            # Loop models in group
            if created is True:
                for app_model in GROUPS[group_name]:
                    # Loop permissions in group/model
                    for permission_name in GROUPS[group_name][app_model]:

                        # Generate permission name as Django would generate it
                        name = "Can {} {}".format(permission_name, app_model)
                        print("Creating {}".format(name))

                        try:
                            model_add_perm = Permission.objects.get(name=name)
                        except Permission.DoesNotExist:
                            logging.warning("Permission not found with name '{}'.".format(name))
                            continue

                        new_group.permissions.add(model_add_perm)
