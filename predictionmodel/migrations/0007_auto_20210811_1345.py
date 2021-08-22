# Generated by Django 3.2.6 on 2021-08-11 11:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("datasource", "0003_alter_fhirendpoint_id"),
        ("predictionmodel", "0006_predictionmodelresult"),
    ]

    operations = [
        migrations.AddField(
            model_name="predictionmodelsession",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="predictionmodelsession",
            name="data_source",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="datasource.fhirendpoint",
            ),
        ),
        migrations.AddField(
            model_name="predictionmodelsession",
            name="patient_id",
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]