# Generated by Django 5.1.6 on 2025-02-19 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_userdetails_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
