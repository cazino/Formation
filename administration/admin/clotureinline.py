# -*- coding: utf-8 -*-
from greta.administration.models import Cloture
from django.contrib import admin
from django import forms
import myfields



class ClotureInLine(admin.StackedInline):
    
    class ClotureForm(forms.ModelForm):
        class Meta:
            model = Cloture
        date_abandon = myfields.MyDateField(label=u"Si non, abandon à la date (jj/mm/aaaa)")
        
        def clean(self):
            cleaned_data = self.cleaned_data
            terme = cleaned_data.get("terme")
            date_abandon = cleaned_data.get("date_abandon")
            if terme==False and date_abandon is None:
                raise forms.ValidationError(u"Si la lettre de commande n'est pas arrivée à son terme, précisez la date d'abandon")
            return cleaned_data
                               
        
    model = Cloture
    form = ClotureForm
    extra = 1
    fieldsets = [
        ('Détails',{'fields': ['terme',  'date_abandon', 'motif'], 
                    'classes': ['collapse']}),
    ]
    
