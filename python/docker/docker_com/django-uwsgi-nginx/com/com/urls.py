"""com URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from guo.views import *
from django.conf import settings
from django.views import static
from django.conf.urls import include
from django.conf.urls import handler400, handler403, handler404, handler500

# from tastypie.api import Api

# v1 = Api(api_name='v1')
# v1.register(MesResource())

urlpatterns = [
    path('guoguo/', admin.site.urls),
    path('', index),
    re_path('^Assets/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    path('regist/', register, name='regist'),
    path('login/', login, name='login'),
    path('logout/', logout),
    path('upload/', upload),
    path('search/', search),
    path('userInfo/', info),
    path('change_pass/', change_pass),
    re_path('^media/(?P<path>.*)$', static.serve, {"document_root": settings.MEDIA_ROOT}),
    re_path('^deatil/(?P<id>\d+)/$', deatil),
    # re_path('^api/',include(v1.urls)),
    path('get_more/', get_more),
    path('save_mes/', save_com),
    path('like/', like),
    path('unlike/', unlike),
    path('weibo/', include('social_django.urls', namespace='social')),
    path('send_email/',send_email),
    path('forgot/',forgot),
    path('new_pass/',new_pass),
]

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error
