# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from greta.administration.models import Bilan
import myfields

class bilanInLine(admin.StackedInline):
    
    class bilanForm(forms.ModelForm):
        class Meta:
            model = Bilan
                    
        inscritAle = myfields.MyDateField(label=u"Bénéficiaire inscrite à ALE depuis (jj/mm/aaaa)")
        emploi_debut = myfields.MyDateField(u"Date de début du contrat (jj/mm/aaaa)")
        emploi_fin = myfields.MyDateField(u"Date de fin du contrat (jj/mm/aaaa)")
        form_debut = myfields.MyDateField(label=u"Date d'entrée en stage (jj/mm/aaaa)")
        form_fin = myfields.MyDateField(label=u"Date de fin de stage (jj/mm/aaaa)")
        entr_date = myfields.MyDateField(label=u"A compter du (jj/mm/aaaa)")
        cess_date = myfields.MyDateField(label=u"A compter du (jj/mm/aaaa)")
        action_P1_deb = myfields.MyDateField(u"Période en entreprise 1 - Date de début (jj/mm/aaaa)")
        action_P1_fin = myfields.MyDateField(u"Période en entreprise 1 - Date de fin (jj/mm/aaaa)")
        action_P2_deb = myfields.MyDateField(u"Période en entreprise 2 - Date de début (jj/mm/aaaa)")
        action_P2_fin = myfields.MyDateField(u"Période en entreprise 2 - Date de fin (jj/mm/aaaa)")
        conc_datenext = myfields.MyDateField(u"Date de rendez-vous avec le conseiller prescripteur à l'issue du bilan (jj/mm/aaaa)")
        conc_date = myfields.MyDateField(u"Date de réalisation du bilan (jj/mm/aaaa)")
        conc_obsref = forms.CharField(label=u"Observations du référent: ", 
                                      required=False, 
                                      widget=forms.Textarea(attrs={'wrap':'hard','class': 'vLargeTextField'}))
        
        
    model = Bilan
    form = bilanForm
    fieldsets = [
                 (u"Inscription", {'fields': ['inscritAle'], 'classes': ['collapse']}),
                 (u"Correspondant ALE", {'fields': ['aleCor_nom', 'aleCor_tel', 'aleCor_mail'],
                                         'classes': ['collapse']}),
                                         
                 (u"Situation en fin d'accompagnement - Emploi", {'fields': ['emploi_posteOcc',
                                                                             'emploi_codeRome',
                                                                             'emploi_typeContrat',
                                                                             'emploi_CADetails',
                                                                             'emploi_AUDetails',
                                                                             'emploi_debut',
                                                                             'emploi_fin',
                                                                             'emploi_duree',
                                                                             'emploi_coord',
                                                                             ],
                                                                  'classes': ['collapse']}),
                                                                  
                 (u"Situation en fin d'accompagnement - Formation", {'fields': ['form_intitule',
                                                                                'form_coor',
                                                                                'form_objectif',
                                                                                'form_heure',
                                                                                'form_debut',
                                                                                'form_fin',
                                                                               ],
                                                                    'classes': ['collapse']}),                                                 
                
                (u"Situation en fin d'accompagnement - Création d'entreprise", {'fields': ['entr_nature',
                                                                                           'entr_lieu',
                                                                                           'entr_date',
                                                                                           'entr_justifcatif',
                                                                                           'entr_dossier',
                                                                                           'entr_docs',
                                                                                           ],
                                                                                'classes': ['collapse']}),
                                                                                
                (u"Situation en fin d'accompagnement - Toujours à la recherche d'un emploi", {'fields': ['rech_intit',
                                                                                                         'rech_rome',
                                                                                                         'rech_sect',
                                                                                                         'rech_zone',
                                                                                                         ],
                                                                                            'classes': ['collapse']}),
                                                                                            
                 (u"Situation en fin d'accompagnement - Cessation d'incription", {'fields': ['cess_date',
                                                                                             'cess_moti',
                                                                                            ],
                                                                                 'classes': ['collapse']}),
                                                                                 
                (u"Actions réalisées pendant l'accompagnement - Stabilisation du ou des métiers recherchés/ Elaboration du professionnel (à détailler par rapport aux fichiers ROME des emploi concernés)",
                 
                                                                                 {'fields': ['action_comp',
                                                                                             'action_cogn',
                                                                                             'action_rela',
                                                                                             'action_P1_deb',
                                                                                             'action_P1_fin',
                                                                                             'action_P1_coord',
                                                                                             'action_P1_res',
                                                                                             'action_P1_comp',
                                                                                             'action_P2_deb',
                                                                                             'action_P2_fin',
                                                                                             'action_P2_coord',
                                                                                             'action_P2_res',
                                                                                             'action_P2_comp',
                                                                                            ],
                                                                                 'classes': ['collapse']}),  
                                                                                 
                (u"Actions réalisées pendant l'accompagnement - Accompagnement vers l'emploi/pistes d'emploi",
                 
                                                                                 {'fields': ['action_nbOE',
                                                                                             'action_nbCa',
                                                                                             'action_nbEN',
                                                                                             'action_autreEmp',
                                                                                             'action_autreSect',
                                                                                             'action_autreAct',
                                                                                             'action_sect',
                                                                                            ],
                                                                                 'classes': ['collapse']}),
                                                                                 
               (u"Actions réalisées pendant l'accompagnement - Suivi dans l'emploi",
                 
                                                                                 {'fields': ['action_reprCont',
                                                                                             'action_reprDiff',
                                                                                             'action_reprRep',
                                                                                             'action_reprEntr',
                                                                                             'action_reprMod',
                                                                                            ],
                                                                                 'classes': ['collapse']}), 
                                                                                 
               (u"Actions priorotaires à mener à l'issue de la prestation (pour les personnes n'ayant pas trouvé de solutions (emploi/formation/créations d'entreprises))",
                 
                                                                                 {'fields': ['actionPrio_A1_date',
                                                                                             'actionPrio_A1_action',
                                                                                             'actionPrio_A1_demarche',
                                                                                             'actionPrio_A2_date',
                                                                                             'actionPrio_A2_action',
                                                                                             'actionPrio_A2_demarche',
                                                                                             'actionPrio_A3_date',
                                                                                             'actionPrio_A3_action',
                                                                                             'actionPrio_A3_demarche',
                                                                                            ],
                                                                                 'classes': ['collapse']}),                                                                  
                                                                                                                                                                                                                                                                                               
                                                                                            
               (u"Conclusion", {'fields': ['conc_obsref',
                                           'conc_obsbene',
                                           'conc_datesuivi',
                                           'conc_cons',
                                           'conc_datenext',
                                           'conc_date',
                                          ],
                                'classes': ['collapse']}),                                                          
            
                    ]
    
    
