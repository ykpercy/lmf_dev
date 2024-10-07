from django.core.management.base import BaseCommand
from stock_api.models import StockInfo, StockSpot
import akshare as ak
from django.db import transaction
import concurrent.futures
from django.utils import timezone
import logging

# 设置日志
logger = logging.getLogger('django')

class Command(BaseCommand):
    help = 'Update stock info and spot data using akshare'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update-type',
            type=str,
            help='Specify which update to run: "info", "spot", or "all"'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        update_type = options['update_type']
        # self.stdout.write(f'开始更新股票数据... 时间: {timezone.now()}')
        logger.info(f'开始更新股票数据. 时间: {timezone.now()}')
        if update_type in [None, 'all', 'info']:
            self.update_stock_info()
        if update_type in [None, 'all', 'spot']:
            self.update_stock_spot_data()
        # self.update_stock_info()
        # self.update_stock_spot_data()
        logger.info(f'成功更新所有股票数据. 时间: {timezone.now()}')
        # self.stdout.write(self.style.SUCCESS(f'Successfully updated stock data. 时间: {timezone.now()}'))

    @transaction.atomic
    def update_stock_info(self):
        # self.stdout.write('Updating stock info...')
        logger.info('开始更新股票基本信息')
        try:
            stock_info_origin = ak.stock_zh_a_spot()
            stock_info_origin['代码'] = stock_info_origin['代码'].str.upper()
            stock_info = stock_info_origin.iloc[:, :2].rename(columns={'代码': 'code', '名称': 'name'})

            # 过滤掉名称中包含'退'的股票
            stock_info = stock_info[~stock_info['name'].str.contains('退')]

            # 准备批量插入或更新的数据
            update_data = [
                {
                    'code': row['code'],
                    'name': row['name']
                }
                for _, row in stock_info.iterrows()
            ]

            # 删除数据库中名称包含'退'的股票
            deleted_count = StockInfo.objects.filter(name__contains='退').delete()[0]
            # self.stdout.write(self.style.SUCCESS(f'已删除 {deleted_count} 条包含"退"的股票记录'))
            logger.info(f'已删除 {deleted_count} 条包含"退"的股票记录')
            
            # 使用批量创建或更新
            created, updated = self.bulk_update_or_create(StockInfo, update_data, ['name'], batch_size=512)

            # for _, row in stock_info.iterrows():
            #     code, name = row['code'], row['name']
            #     StockInfo.objects.update_or_create(
            #         code=code,
            #         defaults={'name': name}
            #     )

            # # 删除所有现有的 StockInfo 记录
            # StockInfo.objects.all().delete()
            # self.stdout.write(self.style.SUCCESS('已删除所有现有股票信息')) 
            
            # # 批量创建新的 StockInfo 记录
            # stocks_to_create = [
            #     StockInfo(code=row['code'], name=row['name'])
            #     for _, row in stock_info.iterrows()
            # ]
            
            # # 使用 bulk_create 批量创建新记录
            # StockInfo.objects.bulk_create(stocks_to_create)
            
            # self.stdout.write(self.style.SUCCESS(f'成功创建 {created} 条新的股票信息记录，更新 {updated} 条记录'))
            logger.info(f'成功创建 {created} 条新的股票信息记录，更新 {updated} 条记录')
        except Exception as e:
            logger.error(f'更新股票基本信息时发生错误: {str(e)}')

    def bulk_update_or_create(self, model, data, update_fields, batch_size=512):
        # 获取所有现有的代码
        existing_codes = set(model.objects.values_list('code', flat=True))
        
        # 分离需要更新和插入的数据
        to_update = []
        to_create = []
        for item in data:
            if item['code'] in existing_codes:
                to_update.append(model(**item))
            else:
                to_create.append(model(**item))
        
        # 批量创建新记录
        model.objects.bulk_create(to_create, batch_size=batch_size)
        
        # 批量更新现有记录
        model.objects.bulk_update(to_update, update_fields, batch_size=batch_size)

        return len(to_create), len(to_update)

    def update_single_stock_spot_data(self, stock):
        try:
            spot_data = ak.stock_individual_spot_xq(symbol=stock.code)
            if not spot_data.empty:
                data = spot_data.set_index('item')['value'].to_dict()
                StockSpot.objects.update_or_create(
                    stock=stock,
                    defaults={
                        'current_price': data['现价'],
                        'change': data['涨跌'],
                        'change_percent': data['涨幅'],
                        'volume': data['成交量'],
                        'turnover': data['成交额'],
                        'ytd_change_percent': data['今年以来涨幅'],
                        'currency': data['货币'],
                        'net_assets_per_share': data['每股净资产'],
                        'earnings_per_share': data['每股收益'],
                        'pe_ratio_ttm': data['市盈率(TTM)'],
                        'pe_ratio_static': data['市盈率(静)'],
                        'pe_ratio_dynamic': data['市盈率(动)'],
                        'pb_ratio': data['市净率'],
                        'fund_shares_total_shares': data['基金份额/总股本'],
                        'nav_market_cap': data['资产净值/总市值'],
                    }
                )
            return f'Updated spot data for {stock.code}'
        except Exception as e:
            return f'Error updating {stock.code}: {str(e)}'

    def update_stock_spot_data(self):
        # self.stdout.write(f'Updating stock spot data... 时间: {timezone.now()}')
        logger.info(f'开始更新股票即时数据. 时间: {timezone.now()}')
        # 删除所有现有的 StockSpot 记录
        # StockSpot.objects.all().delete()
        # self.stdout.write(self.style.SUCCESS('已删除所有现有股票估值信息')) 

        stocks = StockInfo.objects.all()
        success_count = 0
        error_count = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_stock = {executor.submit(self.update_single_stock_spot_data, stock): stock for stock in stocks}
            for future in concurrent.futures.as_completed(future_to_stock):
                stock = future_to_stock[future]
                try:
                    result = future.result()
                    # self.stdout.write(result)
                    if "Error" in result:
                        error_count += 1
                    else:
                        success_count += 1
                    logger.info(result)
                except Exception as exc:
                    # self.stdout.write(f'{stock.code} 生成了一个异常: {exc}')
                    error_message = f'{stock.code} 生成了一个异常: {exc}'
                    logger.error(error_message)
                    error_count += 1
        # for stock in stocks:
        #     result = self.update_single_stock_spot_data(stock)
        #     self.stdout.write(result)

        # self.stdout.write(self.style.SUCCESS(f'Finished updating stock spot data. 时间: {timezone.now()}'))
        logger.info(f'完成更新股票即时数据. 成功: {success_count}, 失败: {error_count}')