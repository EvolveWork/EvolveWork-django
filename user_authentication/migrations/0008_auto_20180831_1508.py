# Generated by Django 2.0.7 on 2018-08-31 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0007_auto_20180831_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='id',
            field=models.CharField(blank=True, max_length=255, primary_key=True, serialize=False),
        ),
    ]
