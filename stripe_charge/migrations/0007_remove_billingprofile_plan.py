# Generated by Django 2.0.7 on 2018-07-27 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_charge', '0006_auto_20180727_1936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingprofile',
            name='plan',
        ),
    ]
