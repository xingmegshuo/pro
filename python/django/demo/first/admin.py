from django.contrib import admin
from first.models import Article
# Register your models here.


class MymodelAdmin(admin.ModelAdmin):
    pass



admin.site.register(Article,MymodelAdmin)