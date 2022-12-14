# Generated by Django 4.1.3 on 2022-12-03 18:12

from django.db import migrations, models
import medcenter.validators


class Migration(migrations.Migration):

    dependencies = [
        ('medcenter', '0003_alter_customuser_usermobile_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='UserMobile_Phone',
            field=models.CharField(blank=True, help_text='Not required. Standart format is -> +XXX (XX) XXX-XXX-XXXX', max_length=32, validators=[medcenter.validators.validate_phone], verbose_name='Mobile phone'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, db_column='UserEmail', max_length=128, validators=[medcenter.validators.validate_email]),
        ),
    ]
