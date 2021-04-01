from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import tb_news
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
import requests
import json
from django.utils.html import strip_tags


# Create your views here.


def handler500(request):
    return render(request, 'Mywebsite/404error.html')


def handler404(request, exception):
    return render(request, 'Mywebsite/404error.html')


def index(request):
    content = tb_news.objects.all().order_by("-id")
    return render(request, 'Mywebsite/index.html', {'news': content})


@login_required(login_url='/login')
@permission_required('is_staff', login_url='/warning')
def addnews(request):
    return render(request, 'Mywebsite/addnews.html')




def addnewsdata(request):
    news_title = request.POST['news_title']
    news_title =strip_tags(news_title)
    news_detail = request.POST['news_detail']
    news_photo = request.FILES['news_photo']
    content = tb_news(news_title=news_title,
                      news_detail=news_detail, news_photo=news_photo)
    content.save()
    return redirect("/contentmanager")


@login_required(login_url='/login')
@permission_required('is_staff', login_url='/warning')
def contentmanager(request):
    mydatanews = tb_news.objects.all().order_by("-id")
    return render(request, 'Mywebsite/contentnewsmanager.html', {'news': mydatanews})


def contentedit(request):
    title = request.GET['title']
    result = tb_news.objects.filter(news_title=title)
    if result:
        return render(request, 'Mywebsite/contentedit.html', {'result': result})
    else:
        return render(request, 'Mywebsite/404error.html')


def contentupdate(request):
    id = request.POST['id']
    news_title = request.POST['news_title']
    news_detail = request.POST['news_detail']
    try:
        news_photo = request.FILES['news_photo']
    except KeyError:
        news_photo = None
    content = tb_news.objects.get(pk=id)
    content.news_title = news_title
    content.news_detail = news_detail
    if news_photo is not None:
        content.news_photo = news_photo
    content.save()
    return redirect("/contentmanager")


def contentdelete(request):
    id = request.POST['id']
    content = tb_news.objects.get(pk=id)
    content.delete()
    return redirect("/contentmanager")


def contentresult(request):
    title = request.GET['title']
    content = tb_news.objects.filter(news_title=title)
    if content:
        return render(request, 'Mywebsite/result.html', {'result': content})
    else:
        return render(request, 'Mywebsite/404error.html')


def regisuser(request):
    return render(request, 'Mywebsite/regisuser.html')


def regisuserdata(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    repassword = request.POST['repassword']
    if password == repassword:
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username ซ้ำในระบบ")
            return redirect("/regisuser")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email ซ้ำในระบบ")
            return redirect("/regisuser")
        else:
            user = User.objects.create_user(
                first_name=fname,
                last_name=lname,
                username=username,
                password=password,
                email=email
            )
            user.save()
            return redirect("/")
    else:
        messages.error(request, "Password และ Repassword ไม่ตรงกัน")
        return redirect("/regisuser")


def login(request):

    if request.user.is_authenticated:
        return redirect("/")
    return render(request, 'Mywebsite/login.html')


def logincheck(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        print(request.user.last_name)
        return redirect('/')
    else:
        messages.error(request, "ไม่พบผู้ใช้งานในระบบ")
        return redirect('/login')


def logoff(request):
    auth.logout(request)
    return redirect("/login")


def warning(request):
    return render(request, 'Mywebsite/warning.html')

def covid19(request):
    url = "https://covid19.th-stat.com/api/open/today"
    res = json.loads(requests.get(url).text)
    print(res)
    return render(request,'Mywebsite/covid19.html',{'covid19':res})
