# Generated by Django 3.1.1 on 2021-02-22 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_resources', '0002_auto_20210222_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='email',
            field=models.EmailField(max_length=30),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
