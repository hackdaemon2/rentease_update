# Generated by Django 2.2.2 on 2019-06-25 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_auto_20190623_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11),
        ),
    ]
