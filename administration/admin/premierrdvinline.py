# -*- coding: utf-8 -*-
from greta.administration.models import ouvertureRdv
from django.contrib import admin

class ouvertureRdvInLine(admin.StackedInline):
     model = ouvertureRdv
     extra = 1
     fieldsets = [
        ('Détails',{'fields': ['dateheure',  'statut'], 'classes': ['collapse']}),
    ]
     list_display = ['dateheure', 'statut']
     

