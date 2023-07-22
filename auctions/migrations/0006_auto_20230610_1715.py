# Generated by Django 3.2.12 on 2023-06-10 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listings_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='image',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='listings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
