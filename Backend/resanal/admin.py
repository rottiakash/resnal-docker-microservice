# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Result, Fetch, Analize
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.



class ResultResource(resources.ModelResource):

    class Meta:
        model = Result



class ResultAdmin(ImportExportModelAdmin):
    resource_class = ResultResource
    pass

admin.site.register(Result,ResultAdmin)
admin.site.register(Fetch)
admin.site.register(Analize)
