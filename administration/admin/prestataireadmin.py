# -*- coding: utf-8 -*-
from greta.administration.models import Prestataire
from django.contrib import admin
from siteinline import SiteInLine

class prestataireAdmin(admin.ModelAdmin):

     inlines = [SiteInLine,]
     
     fieldsets = [
        (None, {'fields': ['nom']}),
        ('Cfc', {'fields': ['cfc_nom', 'cfc_prenom', 'cfc_telfixe', 'cfc_telmobile', 'cfc_fax', 'cfc_mail'], 'classes': ['collapse']}),
        ('Caf', {'fields': ['caf_nom', 'caf_prenom', 'caf_telfixe', 'caf_telmobile', 'caf_fax', 'caf_mail'], 'classes': ['collapse']}),
        ('Coordinateur', {'fields': ['coor_nom', 'coor_prenom', 'coor_telfixe', 'coor_telmobile', 'coor_fax', 'coor_mail'], 'classes': ['collapse']}),
    ]
     #search_fields = ['nom','prenom','polemploi_id'] 
     #list_display = ['nom','prenom','polemploi_id']
     ordering = ['nom',]

admin.site.register(Prestataire,prestataireAdmin)

