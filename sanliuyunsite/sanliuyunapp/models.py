from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    belong_to = models.OneToOneField(to=User ,related_name='user_profile')
    avatar = models.FileField(upload_to='avatar',null = True , blank= True , verbose_name='头像')
    email_address = models.EmailField(verbose_name='邮箱')
    nickname = models.CharField(max_length= 12,verbose_name='昵称')
    def __str__(self):
        return self.nickname

class Article(models.Model):
    author = models.ManyToManyField(to=Person,related_name='article_author')
    headline = models.CharField(max_length= 50,verbose_name='标题')
    text = models.TextField(verbose_name='编辑文档',null = True , blank= True)
    save_time = models.DateTimeField(auto_now=True)#最后保存时间
    local_article = models.FileField(upload_to='localArt',null = True , blank= True , verbose_name='上传本地文档')
    is_write = models.BooleanField(default=False)#是否有成员编辑

    font_size_choices = (
    (3,3),
    (5,5),
    (8,8),
    (20,20),
    (56,56),
    )
    font_size = models.IntegerField(default=5,choices=font_size_choices)
    font_color_choices=(
    ('black','black'),
    ('red','red'),
    ('green','green'),
    ('blue','blue'),
    ('yellow','yellow'),
    )
    font_color = models.CharField(max_length=20,choices=font_color_choices,default='black')
    def __str__(self):
        return self.headline
