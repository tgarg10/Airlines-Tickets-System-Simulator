# Generated by Django 3.2.2 on 2021-06-16 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minesite', '0020_flightdetails_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightdetails',
            name='role',
        ),
    ]
