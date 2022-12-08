# Generated by Django 4.1.3 on 2022-12-07 16:25

from django.db import migrations, models
import medcenter.validators


class Migration(migrations.Migration):

    dependencies = [
        ('medcenter', '0009_userappointment_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertransaction',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='usertransaction',
            name='empid',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='UserMobile_Phone',
            field=models.CharField(blank=True, help_text='Not required. Standart format is -> +XXX (XX) XXX-XX-XX', max_length=32, validators=[medcenter.validators.validate_phone], verbose_name='Mobile phone'),
        ),
        migrations.DeleteModel(
            name='UserAccount',
        ),
        migrations.DeleteModel(
            name='UserTransaction',
        ),
    ]
