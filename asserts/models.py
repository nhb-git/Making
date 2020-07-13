from django.db import models


class Assert(models.Model):
    name = models.CharField(verbose_name='资产名称', max_length=64, unique=True)
    assert_type_choices = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        # ('switch', '交换机'),
        # ('router', '路由器'),
        # ('firewall', '防火墙'),
        ('software', '软件资产'),
        # ('other', '其他')
    )
    assert_type = models.CharField(
        verbose_name='资产类型', choices=assert_type_choices, default='server', max_length=6
    )
    sn = models.CharField(verbose_name='资产sn号', max_length=128, unique=True)
    management_ip = models.GenericIPAddressField(verbose_name='管理ip', null=True, blank=True)
    contract_id = models.ForeignKey('Contract', verbose_name='合同', null=True, blank=True)
    trade_date = models.DateField(verbose_name='购买时间', null=True, blank=True)
    expire_date = models.DateField(verbose_name='过保时间', null=True, blank=True)
    price = models.FloatField(verbose_name='价格', null=True, blank=True)
    admin = models.ForeignKey('UserProfile', verbose_name='资产管理员', null=True, blank=True)
    idc = models.ForeignKey('IDC', verbose_name='机房', null=True, blank=True)
    tags_id = models.ManyToManyField('Tag', verbose_name='标签', blank=True)
    business_unit_id = models.ForeignKey('BusinessUnit', verbose_name='所属业务线', null=True, blank=True)
    manufactory = models.ForeignKey('Manufactory', verbose_name='制造厂商名称', null=True, blank=True)

    meno = models.TextField(verbose_name='备注', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', blank=True, auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', blank=True, auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'

    def __str__(self):
        return '<id:%s name:%s>' % (self.id, self.name)


class Manufactory(models.Model):
    name = models.CharField(verbose_name='厂商名称', max_length=64, unique=True)


class Contract(models.Model):
    pass


class BusinessUnit(models.Model):
    pass


class UserProfile(models.Model):
    pass


class IDC(models.Model):
    pass


class Tag(models.Model):
    pass
