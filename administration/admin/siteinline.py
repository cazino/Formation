# -*- coding: utf-8 -*-
from greta.administration.models import Site
from django.contrib import admin

class SiteInLine(admin.StackedInline):
     model = Site
     extra = 4
     fieldsets = [
        ('Site',{'fields': ['nom', 'adresse', 'codepostal', 'ville', 'telephone'], 'classes': ['collapse']}),
    ]
