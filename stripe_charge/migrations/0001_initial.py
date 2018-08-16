# Generated by Django 2.0.7 on 2018-07-29 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillingProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('name', models.CharField(max_length=255)),
                ('stripeId', models.CharField(max_length=255)),
                ('stripeBillingAddressLine1', models.CharField(max_length=255)),
                ('zipCode', models.CharField(default=None, max_length=255)),
                ('billingAddressState', models.CharField(default=None, max_length=255)),
                ('billingAddressCity', models.CharField(default=None, max_length=255)),
                ('billingAddressCountry', models.CharField(default=None, max_length=255)),
            ],
        ),
    ]
