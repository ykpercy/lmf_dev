# Generated by Django 5.0.6 on 2024-07-03 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0006_remove_stockdata_stock_api_s_is_acti_2748e0_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockInfo',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'cn_stock_instruments',
            },
        ),
        migrations.CreateModel(
            name='StockSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='现价')),
                ('change', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='涨跌')),
                ('change_percent', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='涨幅')),
                ('volume', models.BigIntegerField(verbose_name='成交量')),
                ('turnover', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='成交额')),
                ('ytd_change_percent', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='今年以来涨幅')),
                ('currency', models.CharField(max_length=10, verbose_name='货币')),
                ('net_assets_per_share', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='每股净资产')),
                ('earnings_per_share', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='每股收益')),
                ('pe_ratio_ttm', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='市盈率(TTM)')),
                ('pe_ratio_static', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='市盈率(静)')),
                ('pe_ratio_dynamic', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='市盈率(动)')),
                ('pb_ratio', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='市净率')),
                ('fund_shares_total_shares', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='总股本')),
                ('nav_market_cap', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='总市值')),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
            ],
            options={
                'db_table': 'cn_stock_quotes_valuation',
            },
        ),
        migrations.RenameIndex(
            model_name='stockdata',
            new_name='stock_zh_a__code_2310d8_idx',
            old_name='stock_api_s_code_61ccd0_idx',
        ),
        migrations.RemoveField(
            model_name='stockdata',
            name='is_active',
        ),
        migrations.AlterModelTable(
            name='stockdata',
            table='stock_zh_a_spot_em',
        ),
        migrations.AddIndex(
            model_name='stockinfo',
            index=models.Index(fields=['code'], name='cn_stock_in_code_c66c77_idx'),
        ),
        migrations.AddField(
            model_name='stockspot',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_api.stockinfo', verbose_name='代码'),
        ),
    ]
