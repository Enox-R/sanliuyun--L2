from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponse,StreamingHttpResponse
from sanliuyunapp.form import registerForm,loginForm, ArticleForm,uploadArtForm,addForm
from sanliuyunapp.models import Person, Article
from django.core.exceptions import ObjectDoesNotExist,ValidationError

def indexView(request):
    context = {}
    return render(request,'index.html',context)

def uploadView(request):
    context = {}
    if request.method == 'GET':
        form = uploadArtForm
    if request.method == 'POST':
        form = uploadArtForm(request.POST,request.FILES)
        if form.is_valid():
            user_id = request.user.user_profile.id
            upload_art = request.FILES['uploadArt']
            headline = upload_art.name.split('.')[0]
            art = Article(headline = headline,local_article=upload_art)
            art.save()
            art.author.add(user_id)
            art.save()
            try:
                target = "sanliuyunapp/static/uploads/localArt/{}".format(upload_art.name)
                with open(target,'r') as fs:
                    text = fs.read()
            except FileNotFoundError:
                return HttpResponse('文件名不能包含空格，点等特殊字符')
            fs.close()
            art.text = text
            art.save()

            return redirect(to='desktop')
    context['form'] = form
    return render(request,'upload.html',context)

def downloadArtView(request,art_name):
    context = {}
    user_id = request.user.id
    headline = art_name
    art = Article.objects.get(id = art_name)
    content = art.text
    target = "{}.doc".format(headline)
    with open(target,'w') as fs:
        for chunk in content:
            fs.write(chunk)
        fs.close()
        return HttpResponse('已经导出到项目根目录')
    return render(request,'desktop.html',context)



@login_required(redirect_field_name='login',login_url='login')
def desktopView(request):
    context = {}
    user_id = request.user.user_profile.id
    print(user_id)
    art = Article.objects.filter(author = user_id).order_by('-save_time')
    page_robot = Paginator(art,15)
    page_num = request.GET.get('page')
    if page_num:
        page = int(page_num)
    else:
        page = 1#不加index 跳转进来会报错
    try:
        art = page_robot.page(page_num)
    except EmptyPage:
        art = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        art = page_robot.page(1)
    if page == int(page_robot.num_pages):
        page_range = page_robot.page_range[page-5:page_robot.num_pages]
    elif page == int(page_robot.num_pages)-1:
        page_range = page_robot.page_range[page-4:page_robot.num_pages+1]
    elif page <= 2:
        page_range = page_robot.page_range[0:5-page+page]
    else:
        page_range = page_robot.page_range[page-3 :page+2]
    context['art'] =art
    context['page_range'] =page_range

    return render(request,'desktop.html',context)

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
                login(request,user)
                return redirect(to = 'index')

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
            password2 = form.cleaned_data['password2']
            nickname = form.cleaned_data['nickname']
            email_address = form.cleaned_data['email_address']

            new_Person = User.objects.create_user(username=nickname,email=email_address,password = password2)
            new_Person.save()
            person = Person(belong_to= new_Person,nickname=nickname,email_address= email_address)
            person.save()
            user = authenticate(username =nickname,password = password2)
            login(request,user)
            return redirect(to = 'index')


    context['form']= form
    return render(request,'register.html',context)

@login_required(redirect_field_name='login',login_url='login')
def deleteArtView(request,art_name):
    context = {}
    try:
        art_del = Article.objects.get(id = art_name)
        if request.method == 'GET':
            user_id = request.user.user_profile.id
            art = Article.objects.filter(author = user_id).order_by('-save_time')
            page_robot = Paginator(art,15)
            page_num = request.GET.get('page')
            if page_num:
                page = int(page_num)
            else:
                page = 1#不加index 跳转进来会报错
            try:
                art = page_robot.page(page_num)
            except EmptyPage:
                art = page_robot.page(page_robot.num_pages)
            except PageNotAnInteger:
                art = page_robot.page(1)
            if page == int(page_robot.num_pages):
                page_range = page_robot.page_range[page-5:page_robot.num_pages]
            elif page == int(page_robot.num_pages)-1:
                page_range = page_robot.page_range[page-4:page_robot.num_pages+1]
            elif page <= 2:
                page_range = page_robot.page_range[0:5-page+page]
            else:
                page_range = page_robot.page_range[page-3 :page+2]
            context['art'] =art
            context['page_range'] =page_range
        if request.method == 'POST':
            art_del.delete()
            return redirect('desktop')

    except:
        return HttpResponse('页面已经删除了~')
    return render(request,'deleteArt.html',context)

def deleteResultView(request):
    context = {}
    return render(request,'deleteResult.html',context)


@login_required(redirect_field_name='login',login_url='login')
def editorView(request,art_name):
    context = {}
    if request.method == 'GET':
        art = Article.objects.get(id = art_name)
        form = ArticleForm(
        initial={'headline':art.headline,'content':art.text}
        )
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            # headline = form.cleaned_data['headline']
            # content = form.cleaned_data['content']
            # art = artold(headline=headline, text=content)
            art = Article.objects.get(id = art_name)
            art.headline = form.cleaned_data['headline']
            art.text = form.cleaned_data['content']
            art.save()
            user_id = request.user.user_profile.id
            art.author.add(user_id)
            art.save()
            return redirect(to='editorAdd',art_name=art_name)

    article = Article.objects.get(id=art_name)
    context['form'] = form
    context['article'] = article

    return render(request, 'editoring.html', context)

# def editorArtView(request,art_name):
#     context = {}
#     if request.method == 'GET':
#         art = Article.objects.get(id = art_name)
#         form = ArticleForm(
#         initial={'headline':art.headline,'content':art.text}
#         )
#     if request.method == 'POST':
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             headline = form.cleaned_data['headline']
#             content = form.cleaned_data['content']
#             art = Article(headline=headline, text=content)
#             art.save()
#             user_id = request.user.user_profile.id
#             art.author.add(user_id)
#             art.save()
#             return redirect('desktop')
#     context['form']=form
#     return render(request,'editoring.html',context)

@login_required(redirect_field_name='login',login_url='login')
def editorNewView(request):
    context = {}
    if request.method == 'GET':
        form = ArticleForm
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            headline = form.cleaned_data['headline']
            content = form.cleaned_data['content']
            art = Article(headline=headline, text=content)
            art.save()
            user_id = request.user.user_profile.id
            art.author.add(user_id)
            art.save()
            a = art.id
            return redirect(to='editorAdd',art_name=a)

    # article = Article.objects.get(id=art_name)
    context['form'] = form
    # context['article'] = article

    return render(request, 'editor_new.html', context)

@login_required(redirect_field_name='login',login_url='login')
def editorAddView(request,art_name):
    context = {}
    if request.method == 'GET':
        form = addForm
        art = Article.objects.get(id = art_name)
    if request.method == 'POST':
        form = addForm(request.POST)
        art = Article.objects.get(id = art_name)
        if form.is_valid():
            adduser = form.cleaned_data['addName']
            try:
                user_judge1 = Person.objects.get(nickname = adduser)

                if user_judge1:
                    user_id = user_judge1.id
                    art.author.add(user_id)
                    art.save()
            except:
                try:
                    user_judge2 = Person.objects.get(email_address = adduser)
                    if user_judge2:
                        user_id = user_judge2.id
                        art.author.add(user_id)
                        art.save()
                except:
                    return HttpResponse('用户名/邮箱不存在')

    # user_id = request.user.id

    context['form'] = form
    context['art'] =art

    return render(request, 'editor_add.html', context)
