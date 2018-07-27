# Generated by Django 2.0.7 on 2018-07-27 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_charge', '0003_auto_20180727_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='billingAddressCity',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='billingprofile',
            name='billingAddressCountry',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='billingprofile',
            name='billingAddressState',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='billingprofile',
            name='zipCode',
            field=models.CharField(default=None, max_length=255),
        ),
    ]