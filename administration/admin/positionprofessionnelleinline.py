# -*- coding: utf-8 -*-
from greta.administration.models import PositionProfessionnelle
from django.contrib import admin

class PositionProfessionnelleInLine(admin.StackedInline):
     model = PositionProfessionnelle
     extra = 1
     fieldsets = [
        ('CV',{'fields': ['metier1', 'contrat1', 'dureemois1', 'dureean1',\
                          'metier2', 'contrat2', 'dureemois2', 'dureean2',\
                          'metier3', 'contrat3', 'dureemois3', 'dureean3'], 'classes': ['collapse']}),
        ('Situation', {'fields': ['qualif', 'cv', 'polemp', 'web',\
                          'web_polemp', 'web_autre', 'web_detail', 'reseau',\
                          'entretien', 'secteurporteur', 'pbmobilite', 'pbage',\
                          'pbqualif', 'tafproxi', 'handicap', 'gardenf', 'cout'], 'classes': ['collapse']})
    ]
