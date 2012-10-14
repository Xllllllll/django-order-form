#! -*- coding: utf-8 -*-
import datetime
from django.db import models
from tinymce import models as tinymce_models
from mysite1.settings import MEDIA_URL
from PIL import Image
from cStringIO import StringIO
from os import path

from django.core.files.uploadedfile import SimpleUploadedFile 

class RichFieldAbstract(models.Model):
    text = tinymce_models.HTMLField('описание', blank=True)
    
    class Meta:
        abstract = True

class TitlePriceActiveAbstract(RichFieldAbstract):
    title = models.CharField(max_length=200, verbose_name=u'Название', blank=False, unique=True)
    price = models.IntegerField(verbose_name=u'Цена', blank=False)
    is_active = models.BooleanField(verbose_name=u'Активный', default=True)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.title

class ObjectDateAbstract(models.Model):
    object = models.ForeignKey('Object', verbose_name=u'Заказчик')
    date = models.DateTimeField(editable=False, verbose_name=u'Дата заказа', default=datetime.datetime.now)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.object.name+' '+self.date.strftime("%d %b %Y")
        
class DesignAbstract(models.Model):
    design = models.ForeignKey('Design', verbose_name=u'Дизайн')
    
    class Meta:
        abstract = True

class Module(TitlePriceActiveAbstract):
    is_core = models.BooleanField(verbose_name=u'Базовый', default=True) 
    
    class Meta:
        verbose_name=u'Модуль'
        verbose_name_plural=u'Модули'
    
class Design(TitlePriceActiveAbstract):

    class Meta:
        verbose_name=u'Дизайн'
        verbose_name_plural=u'Дизайны'
        
    def get_photos(self):
        return DesignGallery.objects.all().filter(design=self.id)

class DesignGallery(models.Model):
    design = models.ForeignKey('Design', verbose_name=u'Дизайн')
    foto = models.ImageField('изображение', upload_to='foto')
    thumb = models.ImageField('миниатюра', upload_to='thumb', blank=True)    
    
    class Meta:
        verbose_name=u'Иллюстрация дизайна'
        verbose_name_plural=u'Иллюстрации дизайна'

    def save(self, force_update=False, force_insert=False, 
            thumb_size=(180,300)):
        if self.foto:
            image = Image.open(self.foto)
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
            image.thumbnail(thumb_size, Image.ANTIALIAS)
            temp_handle = StringIO() # save the thumbnail to memory
            image.save(temp_handle, 'png') #
            temp_handle.seek(0) # rewind the file
            suf = SimpleUploadedFile(path.split(self.foto.name)[-1], temp_handle.read(), content_type='image/png') # save to the thumbnail field
            self.thumb.save(suf.name+'.png', suf, save=False) #
            self.thumbnail_width, self.thumbnail_height = image.size #
        super(DesignGallery, self).save(force_update, force_insert) # save the image object            
        
    def admin_image(self):
        return '<img src="'+MEDIA_URL+'%s"/>' % self.thumb
    admin_image.allow_tags = True
    admin_image.short_description = u'изображение'
        
class Object(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Имя', blank=False)
    email = models.EmailField(verbose_name=u'E-mail')
    tel = models.CharField(max_length=200, verbose_name=u'Телефон', blank=False)
    icq = models.CharField(max_length=200, verbose_name=u'ICQ', blank=True)
    skype = models.CharField(max_length=200, verbose_name=u'Skype', blank=True)
    add_info = models.TextField(verbose_name=u'Дополнительная информация', blank=True)
        
    class Meta:
        verbose_name=u'Заказчик'
        verbose_name_plural=u'Заказчики'
        
    def __unicode__(self):
        return self.name

        
class PreSet(DesignAbstract, RichFieldAbstract):
    title = models.CharField(max_length=200, verbose_name=u'Название', blank=False, unique=True)
    module = models.ManyToManyField('Module', verbose_name=u'Модули', null=True, limit_choices_to={'is_core':False}) 
    
    class Meta:
        verbose_name=u'Готовое предложение'
        verbose_name_plural=u'Готовые предложения'

    def __unicode__(self):
        return self.title
        
    def get_modules(self):
        return self.module.all()
    
class SetOrderModule(models.Model):
    setorder = models.ForeignKey('SetOrder', verbose_name=u'Заказ с выбором')
    module=models.ForeignKey('Module', verbose_name=u'Модуль')
    
    class Meta:
        verbose_name=u'Модуль заказа готового предложения'
        verbose_name_plural=u'Модули заказа готовых предложений'
        
class Order(ObjectDateAbstract):

    class Meta:
        verbose_name=u'Заказ'
        verbose_name_plural=u'Заказы'
            
class SetOrder(Order, DesignAbstract):
    module = models.ManyToManyField('Module', verbose_name=u'Модули', null=True, through='SetOrderModule') 
    
    class Meta:
        verbose_name=u'Заказ с выбором'
        verbose_name_plural=u'Заказы с выбором'
            
class PreSetOrder(Order):
    preset = models.ForeignKey('PreSet', verbose_name=u'Готовое предложение')
    
    class Meta:
        verbose_name=u'Заказ готового предложения'
        verbose_name_plural=u'Заказы готовых предложений'
            
