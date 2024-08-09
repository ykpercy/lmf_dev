from django.core.management import call_command
from django.utils import timezone
import logging

logger = logging.getLogger('stock_api')

# def update_stock_info_daily():
#     logger.info(f"开始更新所有股票数据... 时间: {timezone.now()}")
#     call_command('update_stock_data')
#     logger.info(f"股票数据更新完成. 时间: {timezone.now()}")

def update_stock_info():
    print(f"开始更新股票基本信息... 时间: {timezone.now()}")
    call_command('update_stock_data', update_type='info')
    print(f"股票基本信息更新完成. 时间: {timezone.now()}")

def update_stock_spot_data():
    print(f"开始更新股票即时数据... 时间: {timezone.now()}")
    call_command('update_stock_data', update_type='spot')
    print(f"股票即时数据更新完成. 时间: {timezone.now()}")

def update_all_stock_data():
    print(f"开始更新所有股票数据... 时间: {timezone.now()}")
    call_command('update_stock_data', update_type='all')
    print(f"所有股票数据更新完成. 时间: {timezone.now()}")