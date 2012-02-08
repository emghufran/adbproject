from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from vinyl.models import *

# subclass AjaxSelectAdmin
class RecordAdmin(AjaxSelectAdmin):
    # create an ajax form class using the factory function
    #                     model,fieldlist,   [form superclass]
    form = make_ajax_form(Record,{'owner':'record'})
admin.site.register(Record,RecordAdmin)