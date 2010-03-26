# -*- coding: utf-8 -*-
from greta.administration.models import Mobilite
from django.contrib import admin

class MobiliteInline(admin.StackedInline):
     model = Mobilite
     extra = 1
     fieldsets = [
        ('Mobilité',{'fields': ['permis', 'inscrit_permis', 'aide_permis', 'vehicule', 'vehicule_limite', 'rayon_action', 'autre_transport'], 'classes': ['collapse']}),
    ]
