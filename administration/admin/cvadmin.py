# -*- coding: utf-8 -*-
from greta.administration.models import CV
from django.contrib import admin


class CVInLine(admin.StackedInline):
    
    model = CV
    extra = 1
    
    fieldsets = [(u"Premier CV", {'fields': ['cv1', 'cv1_description'],
                                  'classes': ['collapse']}),
                 (u"Deuxième CV", {'fields': ['cv2', 'cv2_description'],
                                  'classes': ['collapse']}),                            
                 ]                                                                       
