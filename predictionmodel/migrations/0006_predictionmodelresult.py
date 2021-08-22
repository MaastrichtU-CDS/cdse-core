# Generated by Django 3.2.6 on 2021-08-10 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("predictionmodel", "0005_rename_child_predictionmodeldata_child_parameter"),
    ]

    operations = [
        migrations.CreateModel(
            name="PredictionModelResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("system", models.CharField(max_length=2048)),
                ("code", models.CharField(max_length=64)),
                ("parameter", models.CharField(max_length=2048)),
                ("calculated_value", models.CharField(max_length=2048)),
                (
                    "session",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="predictionmodel.predictionmodelsession",
                    ),
                ),
            ],
        ),
    ]