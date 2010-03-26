# -*- coding: utf-8 -*-
from greta.administration.models import Statistique
from greta.administration.stat.sortie import StatDoc
from django.contrib import admin
from django import forms
import myfields
from django.http import HttpResponse


class StatAdmin(admin.ModelAdmin):
    
    class StatForm(forms.ModelForm):
        
        class Meta:
            model = Statistique
            
        debut = myfields.MyDateField(label=u"Date de début (jj/mm/aaaa)")
        fin = myfields.MyDateField(label=u"Date de fin (jj/mm/aaaa)")
        
        
    model = Statistique
    form = StatForm
    
    actions = ['stats', ]
    
    def stats(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, u"Veuillez sélectionner une seule ligne")
        else:
            stat = queryset.get()
            response = HttpResponse(mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename='+stat.nom+'.pdf'
            StatDoc(response, stat).build_doc()
            return response
        #self.message_user(request, msg)
    stats.short_description = u"Générer les statistiques"

admin.site.register(Statistique, StatAdmin)
        


    
