from django.shortcuts import render
from first.models import Article
# Create your views here.
import xlrd
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
from first.deal_with import *
import pyLDAvis
import json
from django.contrib.auth import authenticate
from django.shortcuts import redirect

# # 展示数据内容
# def this(request):
#     mes = Article.objects.all()
#     return render(request, 'mian.html', {'mes': mes})
#
#
# 展示分析结果
def show(request):
    return render(request, 'login.html')


def login(request):
    account = request.POST.get('account','')
    password = request.POST.get('password','')
    print(account,password)
    user = authenticate(username=account,password=password)
    if user is not None:
        print('ok')
        mes = Article.objects.all()
        return render(request, 'mian.html', {'mes': mes})
        # return HttpResponse(200)
    else:
        return render(request,'login.html',{'mes':'账号密码错误'})



# 上传excel保存到数据库
def upload(request):
    '''
    :param request:
    :return: 上传文件excel表格 ,并进行解析
    '''
    if request.method == "POST":
        f = request.FILES['my_file']
        type_excel = f.name.split('.')[1]
        if 'xlsx' == type_excel:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read(), )  # 关键点在于这里
            table = wb.sheets()[0]
            nrows = table.nrows  # 行数
            ncole = table.ncols  # 列数
            for i in range(1, nrows):
                rowValues = table.row_values(i)  # 一行的数据
                if not Article.objects.filter(title=rowValues[0]):
                    try:
                        Article.objects.create(title=rowValues[0], content_url=rowValues[1], p_date=rowValues[2][:10],
                                               read_num=int(rowValues[3]), like_num=int(rowValues[4]), comment_num=
                                               int(rowValues[5]), reward_num=int(rowValues[6]), author=rowValues[-3],
                                               source_url=rowValues[-2], content=rowValues[-1]
                                               )
                    except:
                        pass
                    # print(i,rowValues[10])
            return HttpResponseRedirect('/index/')

        return JsonResponse({'msg': '上传文件格式不是xlsx'})

    else:
        return render(request, 'file.html')


# 接收参数数据库查询
def search(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        result = Article.objects.filter(content__icontains=text)
        data = load_data(result)
        title, score = emotion_analysis(data)
        article, reward = reward_analysis(data)
        content, like = like_analysis(data)
        article1, read = read_analysis(data)
        date,read1 = time_analysis(data)
        like_all = [[i[6],i[3]] for i in data]
        try:
            wordlist = tf_word(data)
            return render(request,'data.html', {'title': title, 'score': score, 'article': article, 'reward': reward,'content':
                                content,'like':like,'article1':article1,'read':read,'date':date,'read1':read1,'like_all':like_all,
                                'wordlist':wordlist,
                                })

        except:
            return render(request,'data.html', {'title': title, 'score': score, 'article': article, 'reward': reward,'content':
                                content,'like':like,'article1':article1,'read':read,'date':date,'read1':read1,'like_all':like_all,
                                })


def show_pic(request):
    text = request.GET.get('demo')
    # print(text)
    return_json = {'ok':'ok'}
    result = Article.objects.filter(content__icontains=text)
    data = load_data(result)
    data = make_html(data)
    # print('w2ww')
    pyLDAvis.show(data)
    return HttpResponse(json.dumps(return_json),content_type='application/json')



