from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.http import HttpResponse
from sanliuyunapp.form import registerForm,loginForm, ArticleForm
from sanliuyunapp.models import Person, Article


def indexView(request):
    context = {}
    return render(request,'index.html',context)



def loginView(request):
    context={}
    if request.method == 'GET':
        form = loginForm
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            inputName = form.cleaned_data['inputName']
            password = form.cleaned_data['password']
            user = authenticate(username =inputName,password = password)
            if user:
                login(request,user)
                return redirect(to = 'index')
            else:
                person = Person.objects.get(email_address = inputName)
                inputName = person.nickname
                user = authenticate(username =inputName,password = password)
                if user:
                    login(request,user)
                    return redirect(to = 'index')
                else:
                    return HttpResponse('用户名/密码错误')


            return redirect(to = 'index')
    context['form']= form
    return render(request,'login.html',context)


def registerView(request):
    context={}
    if request.method == 'GET':
        form = registerForm
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            email_address = form.cleaned_data['email_address']
            if nickname ==email_address:
                return HttpResponse('昵称和邮箱地址不能一样哦~')
            try:
                email_judge= Person.objects.get(email_address = email_address )
                if email_judge:
                    return HttpResponse('邮箱重复了~')
            ##判断是否邮箱已经存在
            except:
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 == password2:
                    new_Person = User.objects.create_user(username =nickname,password = password2)
                    new_Person.save()
                    person = Person(belong_to= new_Person,nickname=nickname,email_address= email_address)
                    person.save()
                    user = authenticate(username =nickname,password = password2)
                    if user:
                        login(request,user)
                        return redirect(to = 'index')

                else:
                    return HttpResponse('2次密码不同，请重新输入')
    context['form']= form
    return render(request,'register.html',context)


def editorView(request):

    context = {}
    if request.method == 'GET':
        form = ArticleForm
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            headline = form.cleaned_data['headline']
            content = form.cleaned_data['content']
            a = Article(headline=headline, text=content)
            a.save()


    # article = Article.objects.get()
    context['form'] = form
    # context['article'] = article
    editor_page = render(request, 'editoring.html', context)

    return editor_page
