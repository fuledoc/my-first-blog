# Generated by Django 2.0.13 on 2019-11-25 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_auto_20191125_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='roles',
            field=models.CharField(choices=[('h', '지난 1시간'), ('y', '지난 1년'), ('admin', '지난 1주'), ('user', '모든날짜'), ('m', '지난 1개\x1d월'), ('d', '지난 1일')], default='user', max_length=10),
        ),
        migrations.AlterField(
            model_name='search',
            name='period',
            field=models.CharField(choices=[('h', '지난 1시간'), ('d9', '매일 9시'), ('y', '지난 1년'), ('w9', '매주 9시'), ('w', '지난 1주'), ('m', '지난 1개\x1d월'), ('t', '모든날짜'), ('d', '지난 1일')], default='t', max_length=10),
        ),
    ]
