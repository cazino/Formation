# -*- coding: utf-8 -*-
from greta.administration.models import Rdv, models_etat
from django.contrib import admin
from django import forms
from datetime import timedelta
import myfields
import feries


class myRdvInLineForm(forms.ModelForm):
    
    class Meta:
        model = Rdv
            
    dateheure = myfields.MySplitDateTimeField(required=True , label=u"Date (jj/mm/aaaa) et heure (hh:mm)")
    

    def clean(self):
        super(myRdvInLineForm, self).clean()
        if self.is_valid():
            rdv = Rdv()
            rdv = forms.models.save_instance(form=self, instance=rdv, commit=False)
            lastDate = rdv.lettre_commande.lastRdvDate()
            newDate = self.cleaned_data["dateheure"].date()    
            if lastDate and rdv.typerdv != models_etat.RDV_HEBDO and (newDate > lastDate):
                newDate = self.cleaned_data["dateheure"].date()
                if feries.intervalle(lastDate, newDate) > 14:
                    raise forms.ValidationError(u"L'intervalle entre deux Rdv ne doit pas dépasser 14 jours")
        return self.cleaned_data 


class rdvInLine(admin.StackedInline):
        
    model = Rdv
    form = myRdvInLineForm
    extra = 15
    fieldsets = [
        (u"Détails",{'fields': ['dateheure', 'present', 'typerdv'],
                    'classes': ['collapse']}),
        (u"Accompagnement social",{'fields': ['accsoc_date1', 'accsoc_insti1', 'accsoc_action1', 'accsoc_results1',\
                                              'accsoc_date2', 'accsoc_insti2', 'accsoc_action2', 'accsoc_results2',\
                                              'accsoc_date3', 'accsoc_insti3', 'accsoc_action3', 'accsoc_results3',\
                                              'accsoc_date4', 'accsoc_insti4', 'accsoc_action4', 'accsoc_results4'],
                                  'classes': ['collapse']}),
        (u"Accompagnement emploi",{'fields': ['accemp_date1', 'accemp_entr1', 'accemp_mod1', 'accemp_results1',\
                                              'accemp_date2', 'accemp_entr2', 'accemp_mod2', 'accemp_results2',\
                                              'accemp_date3', 'accemp_entr3', 'accemp_mod3', 'accemp_results3',\
                                              'accemp_date4', 'accemp_entr4', 'accemp_mod4', 'accemp_results4'],
                                  'classes': ['collapse']}),
         (u"Parcours proposé",{'fields': ['parcours',],
                              'classes': ['collapse']}),                         
                                  
                   ]
        
     


"""
    def clean_dateheure(self):
        #lettre_commande,dateheure = self.cleaned_data["lettre_commande"], self.cleaned_data["dateheure"]
        lastDate = self.instance.lettre_commande.lastRdvDate()
        #myFile = open("/root/greta2/log", "w")
        #myFile.write(';'.join(["%s: %s" % (a,b) for (a,b) in self.cleaned_data.items()]))
        #myFile.write(unicode(lc))
        #myFile.close()
        newDate = self.cleaned_data["dateheure"].date()
        if newDate-lastDate > timedelta(days=14):
            raise forms.ValidationError(u"L'intervalle entre deux Rdv ne doit pas dépasser 14 jours")
        return self.cleaned_data["dateheure"]
    
    
    def clean(self):
        if not self.instance.lettre_commande.etat == u"En cours":
            raise forms.ValidationError(u"Impossible de créer un Rdv pour une lettre de commande qui n'est pas en cours")
        return self.cleaned_data 
    """