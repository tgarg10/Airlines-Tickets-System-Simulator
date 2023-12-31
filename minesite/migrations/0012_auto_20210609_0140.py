# Generated by Django 3.2.2 on 2021-06-08 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minesite', '0011_alter_loginmodel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginmodel',
            name='confirmpassword',
            field=models.CharField(default='NULL', max_length=32),
        ),
        migrations.AlterField(
            model_name='loginmodel',
            name='name',
            field=models.CharField(default='NULL', max_length=32),
        ),
        migrations.AlterField(
            model_name='loginmodel',
            name='password',
            field=models.CharField(default='NULL', max_length=32),
        ),
        migrations.AlterField(
            model_name='loginmodel',
            name='username',
            field=models.CharField(default='NULL', max_length=32),
        ),
    ]
