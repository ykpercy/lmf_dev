# Generated by Django 5.0.6 on 2024-07-14 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0010_alter_stockspot_earnings_per_share_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockspot',
            name='volume',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='成交量'),
        ),
    ]
