# -*- coding: utf-8 -*-
from greta.administration.models import EtatCivil
from django.contrib import admin

class EtatCivilInline(admin.StackedInline):
     model = EtatCivil
     extra = 1
     fieldsets = [
        ('Détails',{'fields': ['date_naissance', 'age', 'lieu_naissance', 'adresse', 'code_postal', 'ville', 'telfixe', 'telmobile', 'mail'],
                    'classes': ['collapse']}
         ),]


