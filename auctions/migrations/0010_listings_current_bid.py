# Generated by Django 3.2.12 on 2023-07-01 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='current_bid',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
