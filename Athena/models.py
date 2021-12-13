from django.db import models

# Create your models here.
from django.db.models import UniqueConstraint


class Stock(models.Model):
    code = models.CharField(verbose_name='代码', max_length=10)
    cn_code = models.CharField(verbose_name='cn_代码', max_length=10)
    name = models.CharField(verbose_name='股票名称', max_length=10)
    category = models.CharField(verbose_name='市场名称', max_length=2)
    tag = models.CharField(verbose_name='类型', max_length=20)

    class Meta:
        indexes = [models.Index(fields=['code', 'cn_code'], name='code_idx'), ]
        UniqueConstraint(fields=['code', ], name='unique_code')
        db_table = 'stock'


class StockInfo(models.Model):
    code = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='交易日期')
    open = models.FloatField(verbose_name='开盘价')
    close = models.FloatField(verbose_name='收盘价')
    zhang_die = models.FloatField(verbose_name='涨跌')
    zhang_die_fu = models.CharField(verbose_name='涨跌幅%', max_length=20)
    highest = models.FloatField(verbose_name='最高')
    lowest = models.FloatField(verbose_name='最低')
    cheng_jiao_liang = models.BigIntegerField(verbose_name='成交量')
    cheng_jiao_e = models.FloatField(verbose_name='成交额（万元）')
    huan_shou_lv = models.CharField(verbose_name='换手率%', max_length=10)

    class Meta:
        unique_together = ['code', 'date']
        indexes = [models.Index(fields=['code', 'date']), ]
        ordering = ('-date', 'code',)
        db_table = 'stock_info'
