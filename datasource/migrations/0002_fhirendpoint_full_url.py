# Generated by Django 3.1.6 on 2021-07-02 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datasource", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="fhirendpoint",
            name="full_url",
            field=models.URLField(
                default="http://localhost:1234/fhir", max_length=2048
            ),
        ),
    ]