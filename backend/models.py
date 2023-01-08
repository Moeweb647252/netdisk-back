from django.db import models

# Create your models here.

class User(models.Model):
  name = models.CharField("用户名", max_length=32)
  password = models.CharField("密码", max_length=32)
  path = models.TextField("用户目录")
  token = models.CharField("Token", max_length=32)
  permissionLevel = models.IntegerField("权限等级", default=0)

  class Meta:
    verbose_name = "用户"
    verbose_name_plural = "用户"

  def __str__(self):
    return self.name

