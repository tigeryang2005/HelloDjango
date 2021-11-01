from django.db import models

# Create your models here.


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
