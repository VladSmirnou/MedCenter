# Generated by Django 4.1.3 on 2022-12-07 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medcenter', '0008_userappointment_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userappointment',
            name='Price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
