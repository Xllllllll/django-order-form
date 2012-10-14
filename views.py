# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from mysite1.order.forms import *
from mysite1.order.models import *

def indexmy(request):    
    return render_to_response('index.html',) 

def order(request, *args, **kwargs):    
    preset_list = PreSet.objects.all()
    core_module_list = Module.objects.all().filter(is_core=True)
    if request.method == 'POST':
        formObject = ObjectForm(request.POST)
        if formObject.is_valid():
            name = formObject.cleaned_data['name']
            email = formObject.cleaned_data['email']
            tel = formObject.cleaned_data['tel']
            icq = formObject.cleaned_data['icq']
            skype = formObject.cleaned_data['skype']
            add_info = formObject.cleaned_data['add_info']
            object = Object(name=name, email=email, tel=tel, icq=icq, skype=skype, add_info=add_info)
            object.save()
            if (formObject.cleaned_data['pc_name'] is not None):
                preset_id = formObject.cleaned_data['pc_name']
                preset_order = PreSetOrder(object=object, preset_id=preset_id)
                preset_order.save()
            else:
                design = formObject.cleaned_data['design']
                set_order = SetOrder(design_id=design.id, object=object)
                set_order.save()
                if (formObject.cleaned_data['module'] is not None):
                    module_list = formObject.cleaned_data['module'] | Module.objects.all().filter(is_core=True)
                else: 
                    module_list = Module.objects.all().filter(is_core=True)
                for module in module_list:
                    set_order_module = SetOrderModule(module_id=module.id, setorder_id=set_order.id)
                    set_order_module.save()
            return render_to_response('thanks.html')
    else:
        formObject = ObjectForm()
    return render_to_response('order.html', {
        'formObject':formObject,'preset_list':preset_list, 
        'core_module_list':core_module_list,
    }, context_instance=RequestContext(request))

