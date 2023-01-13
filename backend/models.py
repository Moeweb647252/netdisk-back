from django.db import models


# Create your models here.

class FileSystem:
    type = models.CharField("类型", max_length="32")
    path = models.TextField("路径")
    user = models.BigIntegerField("所有者", default=-1)
    group = models.BigIntegerField("所有组", default=-1)
    totalSpace = models.BigIntegerField("总空间")
    availableSpace = models.BigIntegerField("可用空间")

    class Meta:
        verbose_name = "文件系统"
        verbose_name_plural = "文件系统"

    def __str__(self):
        if self.type == "group":
            return "组文件系统+" + str(self.group)
        elif self.type == "user":
            return "用户文件系统+" + str(self.user)
        elif self.type == "gshare":
            return "组共享文件系统+" + str(self.group)
        elif self.type == "ushare":
            return "用户文件系统+" + str(self.user)


class User(models.Model):
    name = models.CharField("用户名", max_length=32)
    password = models.CharField("密码", max_length=32)
    token = models.CharField("Token", max_length=32)
    permissionLevel = models.IntegerField("权限等级", default=0)
    userFs = models.ForeignKey(FileSystem, models.DO_NOTHING, verbose_name="用户文件系统", null=True, blank=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField("组名", max_length=128)
    users = models.ManyToManyField(User)
    permissionLevel = models.IntegerField("权限等级", default=0)
    userFs = models.ForeignKey(FileSystem, models.DO_NOTHING, verbose_name="用户文件系统", null=True, blank=True)

    class Meta:
        verbose_name = "组"
        verbose_name_plural = "组"

    def __str__(self):
        return self.name
