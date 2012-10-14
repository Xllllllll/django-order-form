#! -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from mysite1.order.models import *

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name=str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a> %s ' % (image_url, image_url, file_name, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

def formfield_for_dbfield_generic(self, db_field, db_field_name, model, **kwargs):
    if db_field.name == db_field_name:
        request = kwargs.pop("request", None)
        kwargs['widget'] = AdminImageWidget
        return db_field.formfield(**kwargs)
    return super(model,self).formfield_for_dbfield(db_field, **kwargs)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active', 'is_core')
    
class DesignAdmin(admin.ModelAdmin):
    pass
    
class ObjectAdmin(admin.ModelAdmin):
    pass
    
class PreSetAdmin(admin.ModelAdmin):
    list_display = ('design', 'get_modules', 'title')
    # readonly_fields = ('is_preset',)
    def save_model(self, request, obj, form, change):
        super(PreSetAdmin, self).save_model(request, obj, form, change)
        form.cleaned_data['module']=form.cleaned_data['module'] | Module.objects.all().filter(is_core=True)
        form.save_m2m()
        obj.save()
        
class SetOrderModuleInline(admin.TabularInline):
    model = SetOrderModule
    extra= 1
    
class SetOrderAdmin(admin.ModelAdmin):
    inlines = (SetOrderModuleInline,)
    
class PreSetOrderAdmin(admin.ModelAdmin):
    list_display = ('object', 'preset')
    
class OrderAdmin(admin.ModelAdmin): 
    list_display = ('object', 'object_tel', 'object_email', 'order_what')
    list_select_related = True
    def __init__(self, *args, **kwargs):
        super(OrderAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ('order_what', )
    def object_email(self, obj):    
        return '%s'%(obj.object.email)
    def object_tel(self, obj):    
        return '%s'%(obj.object.tel)
    def order_what(self, obj):    
        preseturl = reverse('admin:order_presetorder_change', args=(obj.id,))
        seturl = reverse('admin:order_setorder_change', args=(obj.id,))
        try:
            i = PreSetOrder.objects.get(order_ptr=obj.id).id
            return '<a href="{0}">Заказ готового предложения</a>'.format(preseturl, obj.id)
        except PreSetOrder.DoesNotExist:
            pass
        try:
            i = SetOrder.objects.get(order_ptr=obj.id).id
            return '<a href="{0}">Заказ с выбором</a>'.format(seturl, obj.id)
        except SetOrder.DoesNotExist:
            pass        
    order_what.short_description = "Заказ"
    object_email.short_description = "E-mail"
    object_tel.short_description = "Телефон"
    order_what.allow_tags = True

class DesignGalleryAdmin(admin.ModelAdmin):
    list_display = ('design', 'admin_image', )
    list_display_links = ('design', 'admin_image', )
    def formfield_for_dbfield(self, db_field, **kwargs):
        return formfield_for_dbfield_generic(self, db_field, 'thumb', DesignGalleryAdmin, **kwargs)

admin.site.register(Module, ModuleAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Design, DesignAdmin)
admin.site.register(PreSet, PreSetAdmin)
admin.site.register(SetOrder, SetOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(DesignGallery, DesignGalleryAdmin)
admin.site.register(PreSetOrder, PreSetOrderAdmin)