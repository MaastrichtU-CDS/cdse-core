# Generated by Django 3.2.6 on 2021-08-09 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("predictionmodel", "0002_auto_20210809_1133"),
    ]

    operations = [
        migrations.AddField(
            model_name="predictionmodeldata",
            name="input_parameter",
            field=models.CharField(default="test", max_length=2048),
            preserve_default=False,
        ),
    ]
