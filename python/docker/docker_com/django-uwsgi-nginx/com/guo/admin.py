from django.contrib import admin

# Register your models here.
from guo.models import *


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class userAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class GifAdmin(admin.ModelAdmin):
    list_display = ('id', 'gif')


class ImgAdmin(admin.ModelAdmin):
    list_display = ('id', 'img')


class ComAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class MesAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')

class TagAdmin(admin.ModelAdmin):
    list_display = ('id','tag_name')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('id','type')

admin.site.register(Game, GameAdmin)
admin.site.register(User, userAdmin)
admin.site.register(GameGifFile, GifAdmin)
admin.site.register(GameImgFile, ImgAdmin)
admin.site.register(Company, ComAdmin)
admin.site.register(Message, MesAdmin)
admin.site.register(GameType,TypeAdmin)
admin.site.register(Tag,TagAdmin)
