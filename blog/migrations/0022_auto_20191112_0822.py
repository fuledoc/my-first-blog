# Generated by Django 2.0.13 on 2019-11-11 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20191112_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchcomment',
            name='link',
            field=models.URLField(default=2, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='roles',
            field=models.CharField(choices=[('user', '모든날짜'), ('h', '지난 1시간'), ('y', '지난 1년'), ('d', '지난 1일'), ('admin', '지난 1주'), ('m', '지난 1개\x1d월')], default='user', max_length=10),
        ),
        migrations.AlterField(
            model_name='search',
            name='period',
            field=models.CharField(choices=[('w', '지난 1주'), ('h', '지난 1시간'), ('y', '지난 1년'), ('t', '모든날짜'), ('d', '지난 1일'), ('m', '지난 1개\x1d월')], default='t', max_length=10),
        ),
    ]
