# Generated by Django 3.2.6 on 2021-08-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("predictionmodel", "0014_predictionmodelsession_error"),
    ]

    operations = [
        migrations.AddField(
            model_name="predictionmodelsession",
            name="container_id",
            field=models.CharField(default=None, max_length=64, null=True),
        ),
    ]
