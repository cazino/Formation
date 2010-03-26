# -*- coding: utf-8 -*-
from greta.administration.models import Formation
from django.contrib import admin

class FormationInLine(admin.StackedInline):
     model = Formation
     extra = 1
     fieldsets = [
        ('Formation',{'fields': ['besoin', 'niveau', 'formationtype', 'qualifiante',\
                          'certifiante', 'stage', 'formasend', 'departement', 'presta'], 'classes': ['collapse']}),
    ]
