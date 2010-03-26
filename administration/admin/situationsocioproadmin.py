# -*- coding: utf-8 -*-
from greta.administration.models import SituationSocioPro
from django.contrib import admin
from django import forms
import myfields



class SituationSocioProInLine(admin.StackedInline):
    
    class SituationSocioProForm(forms.ModelForm):
        class Meta:
            model = SituationSocioPro
        
        al_date = myfields.MyDateField(required=False, label=u"Date de début du versement de l'allocation (jj/mm/aaaa)")
            
    model = SituationSocioPro
    form = SituationSocioProForm
    extra = 1
    
    fieldsets = [(u"Allocation", {'fields': ['al_type', 'al_date'],
                                  'classes': ['collapse']}),
                 (u"Situation familiale", {'fields': ['sf_statut', 'sf_nbenfants', 'sf_modegarde'],
                                           'classes': ['collapse']}),
                 (u"Projet professionnel", {'fields': ['pp_sansprojet', 'pp_projet1', 'pp_projet2'],
                                           'classes': ['collapse']}),
                 (u"Mobilité", {'fields': ['mob_permis', 'mob_inscritPermis', 'mob_aidePermis', 'mob_vehicule', 'mob_limiteVehicule', 'mob_rayonAction', 'mob_autreTransport'],
                                           'classes': ['collapse']}),
                 (u"Qualification", {'fields': ['qualif_niveau',],
                                     'classes': ['collapse']}),
                 (u"Expérience professionnelle et formation", {'fields': ['exp_expericence1', 'exp_type1', 'exp_duree1', 'exp_expericence2', 'exp_type2', 'exp_duree2', 'exp_expericence3', 'exp_type3', 'exp_duree3', 'form_formation1', 'form_type1', 'form_formation2', 'form_type2'],
                                                               'classes': ['collapse']}),
                 (u"Autres compétences", {'fields': ['autrComp_ling', 'autrComp_info', 'autrComp_autr'],
                                         'classes': ['collapse']}),                             
                ]
    
       
