# Generated by Django 2.0.13 on 2019-11-10 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_customuser_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='roles',
            field=models.CharField(choices=[('admin', 'ADMIN'), ('user', 'USER')], default='user', max_length=10),
        ),
    ]
