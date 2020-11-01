from django.shortcuts import render
from guo.models import *
# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as l
from django.contrib.auth import logout as lo
from django.views.decorators.cache import cache_page
from django.db.models import Count
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from pure_pagination import Paginator, PageNotAnInteger
from django.core.paginator import Paginator as Pageas
from django.db.models import Avg, Aggregate, Count
from django.core.mail import send_mail
from com.settings import EMAIL_HOST_USER

# from tastypie.resources import ModelResource
#
# class MesResource(ModelResource):
#     class Meta:
#         queryset = Message.objects.all()
#         resource_nam = 'p'
#         filtering = {
#             'game':['icontains']}
#


@receiver(pre_delete, sender=User)
def file_delete(sender, instance, **kwargs):
    instance.img.delete(False)


# 获取首页展示数据
# @cache_page(60*360)


# 进入首页
@csrf_exempt
# @cache_page(60 * 60)
def index(request):
    # 获取所有游戏分类
    types = GameType.objects.all()
    dict = {}
    # 根据游戏分类获取数据展示在首页
    for i in types:
        dict[i.type] = Game.objects.all().filter(type=i.id)[:4]
    import datetime
    from dateutil.relativedelta import relativedelta
    new_game = Game.objects.filter(g_time__gte=(datetime.date.today() - relativedelta(months=+2))).order_by('-g_time')[
               :5]
    hot_game = Game.objects.all().annotate(num_like=Count('like')).order_by('num_like')[:5]
    return render(request, 'index.html', {'type': types, 'game': dict, 'new_game': new_game, 'hot_game': hot_game})


# 账号注册
@csrf_exempt
def register(request):
    account = request.POST.get('account')
    password = request.POST.get('password')
    try:
        User.objects.get(username=account)
        return JsonResponse({'code': 300}, safe=False)
    except:
        if '@' in account:
            u = User(username=account, password=make_password(password), email=account)
            u.save()
        else:
            u = User(username=account, password=make_password(password), phone=account)
            u.save()
        return JsonResponse({'code': 200}, safe=False)


# 登录函数
@csrf_exempt
def login(request):
    account = request.POST.get('account')
    password = request.POST.get('password')
    print(account,password)
    # try:
    u = User.objects.get(username=account)
    if u.check_password(password):
        if u.is_superuser:
            return JsonResponse({'code': 200, 'data': '/guoguo/'})
        else:
            l(request, u,backend='django.contrib.auth.backends.ModelBackend')
            request.session['username'] = account
            return JsonResponse({'code': 200, 'data': '/'}, safe=False)
    else:
        return JsonResponse({'code': 300}, safe=False)
    # except:
    #     return JsonResponse({'code': 400}, safe=False)


# 退出账号
@login_required
def logout(request):
    lo(request)
    return HttpResponseRedirect('/')


# 账号信息完善
@login_required
@csrf_exempt
def info(request):
    username = request.session.get('username', '')
    u = User.objects.get(username=username)
    if request.method == 'GET':
        return render(request, 'user_info.html', {'user': u})
    elif request.method == 'POST':
        u.phone = request.POST.get('phone')
        u.name = request.POST.get('name')
        if request.POST.get('sex') == 'true':
            u.sex = False
        else:
            u.sex = True
        u.email = request.POST.get('email')
        u.save()
        return HttpResponseRedirect('/userInfo/')


@csrf_exempt
@login_required
def change_pass(request):
    u = User.objects.get(username=request.session.get('username'))
    if request.POST.get('sub') == 'true':
        u.is_subscribe = True
    else:
        u.is_subscribe = False
    u.save()
    if u.check_password(request.POST.get('password')):
        u.password = make_password(request.POST.get('new_password'))
        u.save()
        return JsonResponse({'mes': '修改成功,重新登录!', 'data': '/'}, safe=False)
    else:
        return JsonResponse({'mes': '密码输入错误!', 'data': '/userInfo/'}, safe=False)


@login_required
@csrf_exempt
def upload(request):
    user = User.objects.get(username=request.session.get('username'))
    try:
        file_delete(sender=User, instance=user)
        user.img = request.FILES['img']
        user.save()
        return JsonResponse({'mes': '修改头像成功!', 'data': '/userInfo/'}, safe=False)
    except:
        return JsonResponse({'mes': '清先修改图片,然后更改!', 'data': '/userInfo'}, safe=False)


# 搜索框展示游戏
@csrf_exempt
def search(request):
    # 获取搜索框输入从数据库中匹配结果分页返回
    content = request.GET.get('content')
    li = [i.id for i in GameType.objects.filter(Q(type__icontains=content))]
    tag = [i.id for i in Tag.objects.filter(Q(tag_name__icontains=content))]
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    if len(tag) > 0:
        data = Game.objects.filter(tag__in=tag)
        p = Paginator(data, 1, request=request)
        page_obj = p.page(page)
        return render(request, 'search_result.html', {'data': page_obj, 'con': content, 'count': p.count})
    else:
        data = Game.objects.filter(
            Q(type__in=li) |
            Q(name__icontains=content)
        )
        p = Paginator(data, 10, request=request)
        page_obj = p.page(page)
        return render(request, 'search_result.html',
                      {'data': page_obj, 'con': content, 'count': p.count})


@csrf_exempt
def deatil(request, id):
    game = Game.objects.get(id=id)
    imgs = GameImgFile.objects.filter(game=game)
    orther_games = Game.objects.filter(type=game.type).filter(~Q(id=game.id)).order_by('?')[:4]
    aver_score = Message.objects.filter(game=game).aggregate(Avg('score'))
    try:
        score = round(aver_score['score__avg'], 1)
    except:
        score = 0
    try:
        video = GameGifFile.objects.get(game=game)
        return render(request, 'deal.html', {'game': game,
                                             'imgs': imgs, 'orther_game': orther_games, 'video': video,
                                             'aver_score': score})
    except:
        return render(request, 'deal.html', {'game': game,
                                             'imgs': imgs, 'orther_game': orther_games,
                                             'aver_score': score})


@csrf_exempt
def get_more(request):
    game = Game.objects.get(id=request.GET.get('game'))
    mes = Message.objects.filter(game=game).order_by('-M_time')
    try:
        page = request.GET.get('page')
    except PageNotAnInteger:
        page = 1
    p = Pageas(mes, 5)
    try:
        page_obj = p.page(page)
        import collections
        page_value = []
        for i in page_obj.object_list:
            data = {}
            data['score'] = i.score
            data['user_img'] = str(i.user.img)
            data['user_name'] = i.user.name
            data['m_time'] = i.M_time.strftime("%Y-%m-%d, %H:%M %P")
            data['content'] = i.content
            page_value.append(data)
        if len(page_value) > 0:
            return JsonResponse({'data': page_value, 'code': 200}, safe=False)
        else:
            return JsonResponse({'data': page_value, 'code': 400}, safe=False)

    except:
        return JsonResponse({'data': 'None', 'code': 300})


@csrf_exempt
def save_com(request):
    game = Game.objects.get(id=request.POST.get('game'))
    u = User.objects.get(username=request.session.get('username'))
    score = request.POST.get('score')
    content = request.POST.get('content')
    mes = Message(content=content, user=u, game=game, score=score)
    mes.save()
    return JsonResponse({'code': 200})


@csrf_exempt
def like(request):
    game = Game.objects.get(id=request.POST.get('game'))
    u = User.objects.get(username=request.session.get('username'))
    game.like.add(u)
    return JsonResponse({'code': 200, 'data': '/deatil/' + str(game.id) + '/'})


def get_random_code(length=6):
    """获得随机字符串"""
    import random
    code = ''
    choice_str = 'abcdefghijklmnopqrstuvwxyz0123456789'
    for _ in range(length):
        random_str = random.choice(choice_str)
        code += random_str
    return code


@csrf_exempt
def send_email(request):
    email = request.POST.get('email')
    try:
        u = User.objects.get(email=email) if User.objects.get(email=email) else User.objects.get(username=email)
        try:
            c = EnveryEmail.objects.get(user=u)
            import datetime
            if datetime.datetime.now() < c.start + datetime.timedelta(minutes=10):
                return JsonResponse({'code': 400, 'data': '已经发送!'})
            else:
                random_code = get_random_code()
                c.code = random_code
                c.start = datetime.datetime.now()
                c.save()
                title = '萌果果-忘记密码,验证重置'
                mes = 'code:' + random_code + '\n' + '请把此验证码输入网站,有效时间十分钟'
                send_mail(title, mes, EMAIL_HOST_USER, [email], fail_silently=False, )
                return JsonResponse({'code': 200}, safe=False)
        except:
            c = EnveryEmail()
            c.user = u
            random_code = get_random_code()
            title = '萌果果-忘记密码,验证重置'
            c.code = random_code
            c.save()
            mes = 'code:' + random_code + '\n' + '请把此验证码输入网站,有效时间十分钟'
            send_mail(title, mes, EMAIL_HOST_USER, [email], fail_silently=False, )
            return JsonResponse({'code': 200}, safe=False)
    except:
        return JsonResponse({'code': 500, 'data': '无法找回密码!没有此邮箱账号'})


def forgot(request):
    return render(request, 'forgot.html')


@csrf_exempt
def new_pass(request):
    email = request.POST.get('user')
    code = request.POST.get('code')
    passw = request.POST.get('pass')
    u = User.objects.get(email=email) if User.objects.get(email=email) else User.objects.get(username=email)
    e = EnveryEmail.objects.get(user=u)
    import datetime
    if e.code == code and datetime.datetime.now() < e.start + datetime.timedelta(minutes=10):
        u.password = make_password(passw)
        u.save()
        return JsonResponse({'code':200})
    else:
        return JsonResponse({'code':300})

@csrf_exempt
def unlike(request):
    game = Game.objects.get(id=request.POST.get('game'))
    u = User.objects.get(username=request.session.get('username'))
    game.like.remove(u)
    return JsonResponse({'code': 200, 'data': '/deatil/' + str(game.id) + '/'})


def bad_request(request, exception, template_name='errors/page_400.html'):
    return render(request, template_name)


def permission_denied(request, exception, template_name='errors/page_403.html'):
    return render(request, template_name)


def page_not_found(request, exception, template_name='errors/page_404.html'):
    return render(request, template_name)


def server_error(request, template_name='errors/page_500.html'):
    return render(request, template_name)
