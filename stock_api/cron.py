from django.core.management import call_command
from django.utils import timezone
import logging

logger = logging.getLogger('stock_api')

def update_stock_info_daily():
    logger.info(f"开始更新所有股票数据... 时间: {timezone.now()}")
    call_command('update_stock_data')
    logger.info(f"股票数据更新完成. 时间: {timezone.now()}")