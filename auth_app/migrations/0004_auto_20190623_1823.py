# Generated by Django 2.2.2 on 2019-06-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_auto_20190623_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio_data',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
