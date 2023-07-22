# Generated by Django 3.2.12 on 2023-06-09 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20230528_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('initialBid', models.IntegerField()),
                ('image', models.CharField(blank=True, max_length=128)),
                ('category', models.CharField(blank=True, max_length=64)),
                ('description', models.CharField(max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dealer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]