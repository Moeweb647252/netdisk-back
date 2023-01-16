from django.db import models

# Create your models here.

class FileSystem(models.Model):
  type = models.CharField("类型", max_length=32)
  path = models.TextField("路径")
  owner_users = models.ManyToManyField('User', verbose_name="所有者")
  owner_groups = models.ManyToManyField('Group', verbose_name="所有组")
  allowed_users = models.ManyToManyField('User', verbose_name="可访问用户", related_name="allowed_users")
  total_space = models.BigIntegerField("总空间")
  available_space = models.BigIntegerField("可用空间")
  permissions = models.CharField("权限", max_length=16, default="006") # others group user
  device = models.ForeignKey('Device', verbose_name="设备", on_delete=models.CASCADE)
  
  class Meta:
    verbose_name = "文件系统"
    verbose_name_plural = "文件系统"

  def __str__(self):
    if self.type == "group":
      return "组文件系统+"+str(self.owner_groups)
    elif self.type == "user":
      return "用户文件系统+"+str(self.owner_users)
    elif self.type == "gshare":
      return "组共享文件系统+"+str(self.owner_groups)
    elif self.type == "ushare":
      return "用户文件系统+"+str(self.owner_users)

class Device(models.Model):
  name = models.CharField("设备名", max_length=128)
  configures = models.TextField("配置")

class User(models.Model):
  name = models.CharField("用户名", max_length=32)
  password = models.CharField("密码", max_length=32)
  token = models.CharField("Token", max_length=32)
  permission_level = models.IntegerField("权限等级", default=0)
  fs = models.ForeignKey(FileSystem, models.DO_NOTHING, verbose_name="用户文件系统", null=True, blank=True)
  email = models.TextField("邮箱")

  class Meta:
    verbose_name = "用户"
    verbose_name_plural = "用户"

  def __str__(self):
    return self.name
  
class Group(models.Model):
  name = models.CharField("组名", max_length=128)
  users = models.ManyToManyField(User)
  permission_level = models.IntegerField("权限等级", default=0)
  fs = models.ForeignKey(FileSystem, models.DO_NOTHING, verbose_name="用户文件系统", null=True, blank=True)
  admins = models.ManyToManyField(User, related_name="group_admins")
  
  class Meta:
    verbose_name = "组"
    verbose_name_plural = "组"

  def __str__(self):
    return self.name

class Settings(models.Model):
  name = models.CharField("名称", max_length=128)
  value = models.TextField("值")

  class Meta:
    verbose_name = "设置"
    verbose_name_plural = "设置"

  def __str__(self):
    return self.name