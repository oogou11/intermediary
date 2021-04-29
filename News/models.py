
from django.db import models

# Create your models here.
from basedb.models import BaseModel, User
from basedb import storage
from ckeditor_uploader.fields import RichTextUploadingField


class NewsClass(BaseModel):
    """
    文章分类
    """

    group = models.CharField(max_length=20, null=True,
                             blank=True, verbose_name='分组', default='')
    NewsClassId = models.ForeignKey(
        'self', null=True, blank=True, verbose_name='上级分类', on_delete=models.SET_NULL)
    # Model.casecade  删除级联
    NewsClassName = models.CharField(default='未设置',
                                     max_length=100, verbose_name='文章分类')
    images = models.ImageField(storage=storage.ImageStorage(),
                               verbose_name='封面图片', null=True, blank=True, upload_to='website/images')

    def __str__(self):
        return self.NewsClassName

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class News(BaseModel):

    NewsClass = models.ForeignKey(
        NewsClass, null=True, blank=True, verbose_name='文章分类', on_delete=models.SET_NULL)
    NewsTitle = models.CharField(max_length=150, verbose_name='文章标题')
    NewsText = RichTextUploadingField(
        null=True, blank=True, verbose_name='文章详情')
    in_num = models.IntegerField(default=0, verbose_name="阅读数")
    images = models.ImageField(storage=storage.ImageStorage(),
                               verbose_name='封面图片', null=True, blank=True, upload_to='website/images')
    file = models.FileField(storage=storage.ImageStorage(),
                            verbose_name='附件', null=True, blank=True, upload_to='website/files')

    def __str__(self):
        return self.NewsTitle

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class SinglePage(BaseModel):

    code = models.CharField(max_length=150, null=True, unique=True,
                            blank=True, verbose_name='调用代码')

    NewsTitle = models.CharField(max_length=150, verbose_name='文章标题')
    NewsText = RichTextUploadingField(
        null=True, blank=True, verbose_name='文章详情')
    in_num = models.IntegerField(default=0, verbose_name="阅读数")
    images = models.ImageField(storage=storage.ImageStorage(),
                               verbose_name='封面图片', null=True, blank=True, upload_to='website/images')

    file = models.FileField(storage=storage.ImageStorage(),
                            verbose_name='附件', null=True, blank=True, upload_to='website/files')

    def __str__(self):
        return self.NewsTitle

    class Meta:
        verbose_name = "单页"
        verbose_name_plural = verbose_name
