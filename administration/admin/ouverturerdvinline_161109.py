# -*- coding: utf-8 -*-
from greta.administration.models import ouvertureRdv
from django.contrib import admin
from django import forms
import myfields



class ouvertureRdvInLine(admin.StackedInline):
    
    class ouvertureRdvForm(forms.ModelForm):
        class Meta:
            model = ouvertureRdv
        dateheure = myfields.MySplitDateTimeField(required=True, label="Date (jj/mm/aaaa) et heure (hh:mm) ")
        dateheure_nouveauRdv = myfields.MySplitDateTimeField(label="Si report, date et heure du nouveau rendez-vous")
            
    model = ouvertureRdv
    form = ouvertureRdvForm
    extra = 1
    fieldsets = [
        ('Détails',{'fields': ['dateheure',  'statut', 'dateheure_nouveauRdv', 'motif'], 'classes': ['collapse']}),
    ]
    list_display = ['dateheure', 'statut']
     

