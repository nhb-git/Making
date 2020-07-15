from django.db import models
from django.contrib.auth.models import User


class Assert(models.Model):
    """资产表"""
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
        verbose_name='资产类型', choices=assert_type_choices, default='server', max_length=16
    )
    sn = models.CharField(verbose_name='资产sn号', max_length=128, unique=True)
    management_ip = models.GenericIPAddressField(verbose_name='管理ip', null=True, blank=True)
    contract_id = models.ForeignKey('Contract', verbose_name='合同', null=True, blank=True, on_delete=models.CASCADE)
    trade_date = models.DateField(verbose_name='购买时间', null=True, blank=True)
    expire_date = models.DateField(verbose_name='过保时间', null=True, blank=True)
    price = models.FloatField(verbose_name='价格', null=True, blank=True)
    admin = models.ForeignKey('UserProfile', verbose_name='资产管理员', null=True, blank=True, on_delete=models.CASCADE)
    idc = models.ForeignKey('IDC', verbose_name='机房', null=True, blank=True, on_delete=models.CASCADE)
    tags_id = models.ManyToManyField('Tag', verbose_name='标签', blank=True)
    business_unit_id = models.ForeignKey(
        'BusinessUnit', verbose_name='所属业务线', null=True, blank=True, on_delete=models.CASCADE
    )
    manufactory = models.ForeignKey(
        'Manufactory', verbose_name='制造厂商名称', null=True, blank=True, on_delete=models.CASCADE
    )

    meno = models.TextField(verbose_name='备注', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', blank=True, auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', blank=True, auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'

    def __str__(self):
        return '<id:%s name:%s>' % (self.id, self.name)


class Server(models.Model):
    """服务器信息"""
    assert_obj = models.OneToOneField(Assert, on_delete=models.CASCADE)
    sub_assert_type_choices = (
        (0, 'PC服务器'),
        (1, '小型机'),
        (2, '刀片服务器')
    )
    sub_assert_type = models.SmallIntegerField(verbose_name='服务器类型', choices=sub_assert_type_choices, default=0)
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual')
    )
    created_by = models.CharField(verbose_name='被创建的类型', max_length=32, choices=created_by_choices, default='auto')
    hosted_on = models.ForeignKey(
        'self', related_name='hosted_on_server', blank=True, null=True, on_delete=models.CASCADE
    )
    model = models.CharField(verbose_name='型号', max_length=32, null=True, blank=True)
    raid_type = models.CharField(verbose_name='raid类型', max_length=128, null=True, blank=True)

    os_type = models.CharField(verbose_name='操作系统类型', max_length=64, null=True, blank=True)
    os_distribution = models.CharField(verbose_name='发型版本', max_length=64, null=True, blank=True)
    os_release = models.CharField(verbose_name='操作系统版本', max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'

    def __str__(self):
        return '%s sn:%s' % (self.assert_obj.name, self.assert_obj.sn)


class NetworkDevice(models.Model):
    """网络设备"""
    assert_obj = models.OneToOneField(Assert, on_delete=models.CASCADE)
    sub_assert_type_choices = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (3, 'VPN设备')
    )
    sub_assert_type = models.SmallIntegerField(
        verbose_name='网络设备类型', choices=sub_assert_type_choices, default=0
    )
    vlan_ip = models.GenericIPAddressField(verbose_name='VlanIP', null=True, blank=True)
    intranet_ip = models.GenericIPAddressField(verbose_name='内网IP', null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=128, null=True, blank=True)
    firmware = models.CharField(verbose_name='固件', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField(verbose_name='端口个数', null=True, blank=True)
    device_detail = models.TextField(verbose_name='设备详情', null=True, blank=True)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'

    def __str__(self):
        return '%s sn:%s' % (self.assert_obj.name, self.assert_obj.sn)


class Software(models.Model):
    """软件表"""
    software_type_choices = (
        (0, 'OS'),
        (1, '办公\开发软件'),
        (2, '业务')
    )
    software_type = models.CharField(verbose_name='软件类型', choices=software_type_choices, default=0, max_length=16)


class Disk(models.Model):
    """硬盘表"""
    asset = models.ForeignKey('Assert', on_delete=models.CASCADE)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插槽位', max_length=64)
    # manufactory = models.CharField(u'制造商', max_length=64,blank=True,null=True)
    model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    auto_create_fields = ['sn', 'slot', 'manufactory', 'model', 'capacity', 'iface_type']

    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"

    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id, self.slot, self.capacity)


class NIC(models.Model):
    """网卡组件"""
    asset = models.ForeignKey('Assert', on_delete=models.CASCADE)
    name = models.CharField(u'网卡名', max_length=64, blank=True, null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    model = models.CharField(u'网卡型号', max_length=128, blank=True, null=True)
    macaddress = models.CharField(u'MAC', max_length=64, unique=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
    netmask = models.CharField(max_length=64, blank=True, null=True)
    bonding = models.CharField(max_length=64, blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s:%s' % (self.asset_id, self.macaddress)

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u"网卡"
        # unique_together = ("asset_id", "slot")
        unique_together = ("asset", "macaddress")

    auto_create_fields = ['name', 'sn', 'model', 'macaddress', 'ipaddress', 'netmask', 'bonding']


class RAM(models.Model):
    """内存组件"""

    asset = models.ForeignKey('Assert', on_delete=models.CASCADE)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    model = models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(MB)')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ("asset", "slot")

    auto_create_fields = ['sn', 'slot', 'model', 'capacity']


class CPU(models.Model):
    """CPU组件"""

    asset = models.OneToOneField('Assert', on_delete=models.CASCADE)
    cpu_model = models.CharField(u'CPU型号', max_length=128, blank=True)
    cpu_count = models.SmallIntegerField(u'物理cpu个数')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = "CPU部件"

    def __str__(self):
        return self.cpu_model


class RaidAdaptor(models.Model):
    """Raid卡"""

    asset = models.ForeignKey('Assert', on_delete=models.CASCADE)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插口', max_length=64)
    model = models.CharField(u'型号', max_length=64, blank=True, null=True)
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("asset", "slot")


class Manufactory(models.Model):
    name = models.CharField(verbose_name='厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=30, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True)

    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class Contract(models.Model):
    sn = models.CharField(u'合同号', max_length=128, unique=True)
    name = models.CharField(u'合同名称', max_length=64)
    memo = models.TextField(u'备注', blank=True, null=True)
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同详细', blank=True, null=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    license_num = models.IntegerField(u'license数量', blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"

    def __str__(self):
        return self.name


class BusinessUnit(models.Model):
    pass


class UserProfile(User):
    name = models.CharField(verbose_name='用户名', max_length=32)

    def __str__(self):
        return self.name


class IDC(models.Model):
    name = models.CharField(u'机房名称', max_length=64, unique=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class Tag(models.Model):
    """资产标签"""

    name = models.CharField('Tag name', max_length=32, unique=True)
    creator = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventLog(models.Model):
    """事件"""
    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    asset = models.ForeignKey('Assert', on_delete=models.CASCADE)
    component = models.CharField('事件子项', max_length=255, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    user = models.ForeignKey('UserProfile', verbose_name=u'事件源', on_delete=models.CASCADE)
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"

    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background: orange;">%s</span>'
        elif self.event_type == 2:
            cell_html = '<span style="background: yellowgreen;">%s</span>'
        else:
            cell_html = '<span >%s</span>'
        return cell_html % self.get_event_type_display()

    colored_event_type.allow_tags = True
    colored_event_type.short_description = u'事件类型'
