# Generated by Django 2.0.7 on 2018-07-28 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0006_auto_20180728_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='billingAddressCity',
            field=models.CharField(default='Gunnison', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='billingAddressCountry',
            field=models.CharField(default='US', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='billingAddressState',
            field=models.CharField(default='CO', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='stripeBillingAddressLine1',
            field=models.CharField(default='607 N. Iowa st.', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='stripeId',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='zipCode',
            field=models.CharField(default=81230, max_length=255),
            preserve_default=False,
        ),
    ]
