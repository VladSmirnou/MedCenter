# Generated by Django 4.1.3 on 2022-12-03 17:54

from django.db import migrations, models
import medcenter.validators


class Migration(migrations.Migration):

    dependencies = [
        ('medcenter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='UserMobile_Phone',
            field=models.CharField(blank=True, max_length=32, validators=[medcenter.validators.validate_phone], verbose_name='Mobile phone'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, db_column='UserEmail', max_length=128, validators=[medcenter.validators.validate_email]),
        ),
    ]