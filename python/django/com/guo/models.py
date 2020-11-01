from django.db import models
# Create your models here.
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete
import datetime
from dateutil.relativedelta import relativedelta

class User(AbstractUser):
    password = models.CharField(max_length=200, verbose_name='密码')
    name = models.CharField(max_length=50, verbose_name='昵称')
    phone = models.CharField(max_length=50, verbose_name='手机')
    email = models.EmailField(verbose_name='邮箱')
    img = models.FileField(upload_to='user', verbose_name='头像')
    sex = models.BooleanField( verbose_name='性别',null=True)
    is_subscribe = models.BooleanField(default=True, verbose_name='是否同意订阅')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '用户数据'


class GameType(models.Model):
    type = models.CharField(max_length=50, verbose_name='游戏类型')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = '游戏分类'


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, verbose_name='标签名字')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name_plural = '游戏标签'


class Game(models.Model):
    name = models.CharField(max_length=50, verbose_name='游戏名字')
    price = models.IntegerField(null=True, default=0, verbose_name='游戏价格')
    type = models.ForeignKey(GameType, verbose_name='类型', on_delete=models.CASCADE)
    info = models.TextField(verbose_name='游戏简介')
    url = models.CharField(max_length=200, verbose_name='游戏链接')
    g_time = models.DateField(verbose_name='游戏发布时间')
    img = models.ImageField(upload_to='user', verbose_name='游戏图片在首页展示', null=True)
    tag = models.ManyToManyField(Tag, related_name='tags', verbose_name='游戏标签')
    like = models.ManyToManyField(User, verbose_name='喜欢的用户', null=True, blank=True)
    is_delte = models.BooleanField(default=True, verbose_name='是否展示在页面上')
    com = models.CharField(null=True,max_length=200,verbose_name='公司')
    pintai = models.CharField(null=True,max_length=200,verbose_name='运营平台')

    def __str__(self):
        return self.name

    class Meta:
        # verbose_name = '游戏详情'
        verbose_name_plural = '游戏详情'


@receiver(pre_delete, sender=Game)
def GameGifFile_delete(sender, instance, **kwargs):
    instance.img.delete(False)


class GameImgFile(models.Model):
    img = models.FileField(upload_to='img', verbose_name='图片')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '游戏图片'


@receiver(pre_delete, sender=GameImgFile)
def GameImgFile_delete(sender, instance, **kwargs):
    instance.img.delete(False)


class GameGifFile(models.Model):
    gif = models.FileField(upload_to='gif', verbose_name='动画')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '游戏动画'


@receiver(pre_delete, sender=GameGifFile)
def GameGifFile_delete(sender, instance, **kwargs):
    instance.gif.delete(False)


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='合作方名字')
    info = models.TextField(verbose_name='合作方介绍')
    url = models.CharField(max_length=50, verbose_name='合作方链接')
    is_delete = models.BooleanField(default=True, verbose_name='是否展示至页面')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合作伙伴'
        verbose_name_plural = '合作伙伴'


class Message(models.Model):
    content = models.TextField(verbose_name='评论内容')
    M_time = models.DateTimeField(verbose_name='评论时间', default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=True, verbose_name='是否展示在页面')
    score = models.IntegerField(verbose_name='评分', default=0)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '用户评价'



class EnveryEmail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=20,verbose_name='验证码')
    start = models.DateTimeField(default=now,verbose_name='开始时间')
