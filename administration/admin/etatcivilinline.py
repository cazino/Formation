# -*- coding: utf-8 -*-
from django import forms
from greta.administration.models import EtatCivil
from django.contrib import admin
import myfields


"""

"""

class EtatCivilInline(admin.StackedInline):

    class EtatCivilForm(forms.ModelForm):

        class Meta:
            model = EtatCivil
        
        date_naissance = myfields.MyDateField(required=False, label=u"Date de naissance (jj/mm/aaaa)")
        
        
    form = EtatCivilForm
    model = EtatCivil
    extra = 1
    fieldsets = [
        ('Détails',{'fields': ['date_naissance', 'age', 'lieu_naissance', 'adresse', 'code_postal', 'ville', 'telfixe', 'telmobile', 'mail'],
                    'classes': ['collapse']}
         ),]


