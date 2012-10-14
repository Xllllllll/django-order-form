# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

from mysite1.order.models import *

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        r = mark_safe(u'%s %s <span>Цена: <span class="price">%s</span> руб.</span>' % (obj.title, obj.text, obj.price))
        photos = DesignGallery.objects.all().filter(design=obj.id)
        for i in photos:
            r += mark_safe('<a href="/media/%s"><img src="/media/%s" alt="" /></a>' %(i.foto, i.thumb))
        return r
    
class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        r = mark_safe(u'%s %s <span>Цена: <span class="price">%s</span> руб.</span>' % (obj.title, obj.text, obj.price))
        return r
    
class ObjectForm(forms.Form):    
    name = forms.CharField(max_length=200, label=u'Имя')
    email = forms.EmailField(label=u'E-mail')
    tel = forms.CharField(max_length=200, label=u'Телефон')
    icq = forms.CharField(max_length=200, required=False)
    skype = forms.CharField(max_length=200, required=False)
    add_info = forms.CharField(widget=forms.Textarea, required=False, label=u'Дополнительно')
    pc_name = forms.DecimalField(required=False)
    module = MyModelMultipleChoiceField(queryset=Module.objects.all(), label=u'', required=False, widget=forms.CheckboxSelectMultiple(attrs={'class':'set module'}))
    design = MyModelChoiceField(queryset=Design.objects.all(), label=u'', required=False, widget=forms.RadioSelect(attrs={'class':'set design'}), empty_label=None)



        