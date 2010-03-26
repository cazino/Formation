from greta.administration.models import Intervention
from django.contrib import admin

class InterventionInLine(admin.StackedInline):
     model = Intervention
     extra = 1
     fieldsets = [
        ('Intervention',{'fields': ['exist', 'sujet', 'logement', 'demenagement', 'tribunaux', 'tuteur', 'contact_tuteur', 'contrat_insertion', 'suivi', 'suivi_autre', 'suivi_referent'], 'classes': ['collapse']}),        
    ]
