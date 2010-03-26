# -*- coding: utf-8 -*-
from greta.administration.models import Frein
from django.contrib import admin


class FreinInLine(admin.StackedInline):
    
    model = Frein
    extra = 1
    
    fieldsets = [(u"Freins professionnels", {'fields': ['pro1', 'pro2', 'pro3'],
                                             'classes': ['collapse']}),
                 (u"Freins personnels", {'fields': ['perso1', 'perso2', 'perso3'],
                                         'classes': ['collapse']}),
                 (u"Freins sociaux", {'fields': ['socio1', 'socio2', 'socio3'],
                                      'classes': ['collapse']}),
                 (u"Freins emploi", {'fields': ['empl1', 'empl2', 'empl3'],
                                    'classes': ['collapse']}),    
                 (u"Autres freins", {'fields': ['autr',],
                                    'classes': ['collapse']}),                                                                       
                ]
    
    
    