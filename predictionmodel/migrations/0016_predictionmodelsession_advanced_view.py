# Generated by Django 3.2.6 on 2021-08-16 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("predictionmodel", "0015_predictionmodelsession_container_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="predictionmodelsession",
            name="advanced_view",
            field=models.BooleanField(default=False),
        ),
    ]
