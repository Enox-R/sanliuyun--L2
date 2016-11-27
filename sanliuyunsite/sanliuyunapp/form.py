from django import forms
from django.core.exceptions import ValidationError
from sanliuyunapp.models import Person,Article
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
### validation function
def word_length(registerForm):
    if len(registerForm)<6 or len(registerForm)>20:
        raise ValidationError(u'字数请设置在6位到20位之间')

def emailValidation(email_address):
    try:
        email_judge = Person.objects.get(email_address = email_address)
        raise ValidationError(u'邮箱被用过了哦')
    except ObjectDoesNotExist as e:
        pass



def nicknameValidation(nickname):
    try:
        nickname_judge = Person.objects.get(nickname = nickname)
        raise ValidationError(u'用户名重复了~')
    except ObjectDoesNotExist as e:
        pass




class uploadArtForm(forms.Form):
    uploadArt= forms.FileField(label='提交文件')

class loginForm(forms.Form):
    inputName = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder':'昵称/邮箱地址'}),
    max_length=25,
    label='昵称/邮箱地址',
    error_messages={'required': '昵称/邮箱地址不能为空哦~'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs  = {'placeholder':'密码'}),
        max_length=25,
        validators = [word_length],
        label = '密码',
        error_messages={'required': '请填写密码！'},
    )

    def clean(self):
        inputName =  self.cleaned_data.get('inputName')
        password = self.cleaned_data.get('password')
        try: ## nickname存不存在
            person = Person.objects.get(nickname = inputName)
        except:
            try: ## email存不存在
                person = Person.objects.get(email_address = inputName)
            except:
                ## 如果两者都不存在则抛错
                return self.add_error('inputName', ValidationError(u'用户不存在哦～'))
        ## 存在的情况下进行认证
        user = authenticate(username =inputName,password = password)
        if not user:
            inputName = person.nickname
            user = authenticate(username =inputName,password = password)
            if not user:
                return self.add_error('password', ValidationError(u'密码输入不对哦～'))

class registerForm(forms.Form):

    nickname = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder':'昵称'}),
    max_length=25,
    label='昵称',
    error_messages={'required': '昵称不能为空哦~'},
    validators = [nicknameValidation,word_length],
    )
    email_address = forms.CharField(widget=forms.EmailInput(attrs  = {'placeholder':'邮箱地址'}),
                                    label='邮箱地址',
                                    error_messages={'required': '请填写正确的邮箱！'},
                                    validators=[emailValidation,word_length],
                                    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs  = {'placeholder':'密码'}),
        max_length=25,
        label = '密码',
        error_messages={'required': '请填写密码！'},
        validators = [word_length],
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs  = {'placeholder':'确认密码'}),
        max_length=25,
        label = '确认密码',
        error_messages={'required': '请填写密码！'},
        validators = [word_length],

        )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', ValidationError(u'两次密码不一样哦～'))


class addForm(forms.Form):
    addName = forms.CharField(
    widget=forms.TextInput(attrs={'id':'addusers','margin-top':'5px','placeholder':'昵称/邮箱地址'}),
    max_length=25,
    label='昵称/邮箱地址',
    # error_messages={'required': '昵称/邮箱地址不能为空哦~'}
    )

class ArticleForm(forms.Form):
    headline = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'无标题'}),max_length=40)
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':'50','placeholder':'请在此输入正文'}))
