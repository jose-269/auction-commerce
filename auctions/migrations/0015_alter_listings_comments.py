# Generated by Django 3.2.12 on 2023-07-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20230708_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='commenting_user', to='auctions.Comments'),
        ),
    ]
