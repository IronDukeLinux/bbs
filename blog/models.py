from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    """
    用户信息表
    """
    phone = models.CharField(max_length=11, null=True, unique=True)  # 手机号
    avatar = models.FileField(upload_to='avatars/', default='avatars/default.png')  # 用户头像

    blog = models.OneToOneField(to='blog', null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Blog(models.Model):
    """
    博客信息表
    """
    title = models.CharField(max_length=64)  # 博客标题
    theme = models.CharField(max_length=32)  # 博客主题

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """
    个人博客文章分类
    """
    title = models.CharField(max_length=32)  # 分类标题
    blog = models.ForeignKey(to='blog')  # 外键关联博客，一个博客站点可以多个分类

    def __str__(self):
        return '{}-{}'.format(self.blog.title, self.title)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    标签表
    """
    title = models.CharField(max_length=32)  # 标签名
    blog = models.ForeignKey(to='Blog')  # 所属博客

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    文章表
    """
    title = models.CharField(max_length=50)  # 文章标题
    desc = models.CharField(max_length=255)  # 文章描述
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    category = models.ForeignKey(to='Category', null=True)  # 文章分类
    user = models.ForeignKey(to='UserInfo')  # 作者
    tags = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    # 评论数
    comment_count = models.IntegerField(default=0)
    # 点赞数
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    """
    文章详情表
    """
    content = models.TextField()  # 文章内容
    article = models.OneToOneField(to='Article')

    def __str__(self):
        return self.article

    class Meta:
        verbose_name = '文章详情'
        verbose_name_plural = verbose_name


class Article2Tag(models.Model):
    """
    文章和标签的多对多关系表
    """
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')

    def __str__(self):
        return '{}-{}'.format(self.article, self.tag)

    class Meta:
        unique_together = (('article', 'tag'), )
        verbose_name = '文章-标签'
        verbose_name_plural = verbose_name


class ArticleUpDown(models.Model):
    """
    点赞表
    """
    user = models.ForeignKey(to='UserInfo', null=True)
    article = models.ForeignKey(to='Article', null=True)
    is_up = models.BooleanField(default=True)  # 点赞还是踩灭

    def __str__(self):
        return '{}-{}'.format(self.user_id, self.article_id)

    class Meta:
        unique_together = (('article', 'user'), )  # 同一个人只能给一篇文章点一个赞
        verbose_name = '点赞'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论表
    """
    article = models.ForeignKey(to='Article')
    user = models.ForeignKey(to='UserInfo')
    content = models.CharField(max_length=255)  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)

    parent_comment = models.ForeignKey('self', null=True, blank=True)  # 自己关联自己

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
