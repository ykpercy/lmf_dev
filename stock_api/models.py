from django.db import models

# Create your models here.
class StockInfo(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cn_stock_instruments'
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

class StockSpot(models.Model):
    stock = models.ForeignKey(StockInfo, on_delete=models.CASCADE, verbose_name="代码")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="现价")
    change = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="涨跌")
    change_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="涨幅")
    volume = models.BigIntegerField(null=True, blank=True, verbose_name="成交量")
    turnover = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="成交额")
    ytd_change_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="今年以来涨幅")
    currency = models.CharField(max_length=10, verbose_name="货币")
    net_assets_per_share = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="每股净资产")
    earnings_per_share = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="每股收益")
    pe_ratio_ttm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="市盈率(TTM)")
    pe_ratio_static = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="市盈率(静)")
    pe_ratio_dynamic = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="市盈率(动)")
    pb_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="市净率")
    fund_shares_total_shares = models.DecimalField(max_digits=15, decimal_places=2, null=True, verbose_name="总股本")
    nav_market_cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, verbose_name="总市值")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    class Meta:
        db_table = 'cn_stock_quotes_valuation'
    
    def __str__(self):
        return f"{self.stock.code} - {self.timestamp}"

class StockData(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="股票代码")
    name = models.CharField(max_length=100, verbose_name="名称")
    latest_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="最新价")
    change_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="涨跌幅", default=0)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="市盈率-动态")
    total_market_value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="总市值")
    circulating_market_value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="流通市值")
    roe = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="净资产收益率")
    gross_profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="销售毛利率")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    class Meta:
        db_table = 'stock_zh_a_spot_em'
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.symbol} - {self.date}"
    
    
