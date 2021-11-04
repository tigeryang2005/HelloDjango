from django.db import models

# Create your models here.


class Stock(models.Model):
    code = models.CharField(verbose_name='代码', max_length=10)
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


class Books(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    abstract = models.TextField()
    img_url = models.CharField(max_length=150, null=True)
    pub_date = models.DateField()
    price = models.FloatField()


class Student(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(default=24)
    sex = models.CharField(max_length=1, default='0')
    address = models.CharField(max_length=100, null=True)
#     一对多关系
    bid = models.ForeignKey(to='BanJi', on_delete=models.CASCADE, default=1)


class StuInfo(models.Model):
    sid = models.OneToOneField('Student', on_delete=models.CASCADE)
    xueli = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)


class BanJi(models.Model):
    name = models.CharField(max_length=20)


class Teacher(models.Model):
    name = models.CharField(max_length=20)
    bid = models.ManyToManyField(to='BanJi')
