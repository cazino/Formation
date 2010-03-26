# -*- coding: utf-8 -*-
from greta.administration.models import ouvertureRdv
from django.contrib import admin
from django import forms
from django.core.exceptions import ObjectDoesNotExist
import myfields


class ouvertureRdvForm(forms.ModelForm):
    
    class Meta:
        model = ouvertureRdv
        
    dateheure = myfields.MySplitDateTimeField(required=True, label="Date (jj/mm/aaaa) et heure (hh:mm) ")
    dateheure_nouveauRdv = myfields.MySplitDateTimeField(label="Si report, date et heure du nouveau rendez-vous")
    
    def clean(self):
        super(ouvertureRdvForm, self).clean()
        if self.is_valid():
            date_rdv = self.cleaned_data.get('dateheure').date()
            rdv = ouvertureRdv()
            rdv = forms.models.save_instance(form=self, instance=rdv, commit=False)
            try:
                date_lc = rdv.lettre_commande.date_debut
                if date_lc != date_rdv:
                    raise forms.ValidationError(u"Le rdv d'ouverture doit avoir lieu le jour du début de la lettre de commande")
            except ObjectDoesNotExist:
                pass
        return self.cleaned_data


class ouvertureRdvInLine(admin.StackedInline):
              
    model = ouvertureRdv
    form = ouvertureRdvForm
    extra = 1
    fieldsets = [
        ('Détails',{'fields': ['dateheure',  'statut', 'dateheure_nouveauRdv', 'motif'], 'classes': ['collapse']}),
    ]
    list_display = ['dateheure', 'statut']
     

