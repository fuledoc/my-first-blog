# Generated by Django 2.0.13 on 2019-11-11 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20191112_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='roles',
            field=models.CharField(choices=[('d', '지난 1일'), ('user', '모든날짜'), ('m', '지난 1개\x1d월'), ('y', '지난 1년'), ('admin', '지난 1주'), ('h', '지난 1시간')], default='user', max_length=10),
        ),
        migrations.AlterField(
            model_name='search',
            name='period',
            field=models.CharField(choices=[('t', '모든날짜'), ('h', '지난 1시간'), ('w', '지난 1주'), ('d', '지난 1일'), ('y', '지난 1년'), ('m', '지난 1개\x1d월')], default='t', max_length=10),
        ),
        migrations.AlterField(
            model_name='searchcomment',
            name='link',
            field=models.URLField(default=''),
        ),
    ]
