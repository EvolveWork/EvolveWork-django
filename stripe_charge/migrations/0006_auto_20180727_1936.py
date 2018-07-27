# Generated by Django 2.0.7 on 2018-07-27 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_charge', '0005_auto_20180727_1600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingprofile',
            old_name='chargeId',
            new_name='stripeId',
        ),
        migrations.AddField(
            model_name='billingprofile',
            name='plan',
            field=models.CharField(default=None, max_length=50),
        ),
    ]