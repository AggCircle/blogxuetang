from django.db import models
from django.utils.timezone import now
from apps.login.models import User


# Create your models here.
class Tag(models.Model):
    name = models.CharField(verbose_name='标签名', max_length=64)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    # 使对象在后台显示更友好
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '标签名称'  # 指定后台显示模型名称
        verbose_name_plural = '标签列表'  # 指定后台显示模型复数名称
        db_table = "tag"  # 数据库表名


class Category(models.Model):
    name = models.CharField(verbose_name='类别名称', max_length=64)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    class Meta:
        ordering = ['name']
        verbose_name = "类别名称"
        verbose_name_plural = '分类列表'
        db_table = "category"  # 数据库表名

    # 使对象在后台显示更友好
    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    title = models.CharField(verbose_name='标题', max_length=100)
    content = models.TextField(verbose_name='正文', blank=True, null=True)
    status = models.CharField(verbose_name='状态', max_length=1, choices=STATUS_CHOICES, default='p')
    views = models.PositiveIntegerField(verbose_name='浏览量', default=0)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    pub_time = models.DateTimeField(verbose_name='活动时间', blank=True, null=True)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)
    deadline = models.DateTimeField(verbose_name='活动确认截止时间', blank=True, null=True)
    activity_words = models.TextField(verbose_name='活动邮件提示语')
    activity_site = models.TextField(verbose_name='活动地点')
    category = models.ForeignKey(Category, verbose_name='活动系列', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField(Tag, verbose_name='标签集合', blank=True)

    # 使对象在后台显示更友好
    def __str__(self):
        return self.title

    # 更新浏览量
    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 下一篇
    def next_article(self):  # id比当前id大，状态为已发布，发布时间不为空
        return Article.objects.filter(id__gt=self.id, status='p', pub_time__isnull=False).first()

    # 前一篇
    def prev_article(self):  # id比当前id小，状态为已发布，发布时间不为空
        return Article.objects.filter(id__lt=self.id, status='p', pub_time__isnull=False).first()

    class Meta:
        ordering = ['-pub_time']  # 按文章创建日期降序
        verbose_name = '活动'  # 指定后台显示模型名称
        verbose_name_plural = '活动列表'  # 指定后台显示模型复数名称
        db_table = 'article'  # 数据库表名
        get_latest_by = 'created_time'


class CustomerApply(models.Model):
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    send = models.BooleanField(default=False)
    verify = models.CharField(max_length=50,default='noresponse')
    article = models.ForeignKey(Article, verbose_name='活动', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    comment = models.CharField(max_length=50,default='未发送')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = '报名信息'  # 指定后台显示模型名称
        verbose_name_plural = '报名信息'  # 指定后台显示模型复数名称
        db_table = "customerapply"  # 数据库表名

