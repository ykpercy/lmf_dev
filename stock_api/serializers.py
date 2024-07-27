from rest_framework import serializers
from .models import StockInfo, StockSpot, StockData

class StockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = ['code', 'name']

class StockSpotSerializer(serializers.ModelSerializer):
    stock_code = serializers.CharField(source='stock.code')
    stock_name = serializers.CharField(source='stock.name')

    class Meta:
        model = StockSpot
        fields = [
            'stock_code', 'stock_name', 'current_price', 'change', 'change_percent',
            'volume', 'turnover', 'ytd_change_percent', 'currency', 'net_asset_per_share',
            'earnings_per_share', 'pe_ratio_ttm', 'pe_ratio_static', 'pe_ratio_dynamic',
            'pb_ratio', 'fund_shares_total_shares', 'net_asset_market_cap_ratio', 'timestamp'
        ]

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['code', 'name', 'latest_price', 'change_percent', 'pe_ratio', 
                  'total_market_value', 'circulating_market_value', 'roe', 
                  'gross_profit_margin', 'last_updated']