# Generated by Django 3.2.6 on 2021-08-11 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "predictionmodel",
            "0012_rename_child_parameter_predictionmodelresult_parent_parameter",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="predictionmodelsession",
            name="calculation_complete",
            field=models.BooleanField(default=False),
        ),
    ]
