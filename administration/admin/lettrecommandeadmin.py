# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import admin
from django import forms
from rdvinline import rdvInLine
from ouverturerdvinline import ouvertureRdvInLine
from etatcivilinline import EtatCivilInline
from bilaninline import bilanInLine
from situationsocioproadmin import SituationSocioProInLine
from freinadmin import FreinInLine
from cvadmin import CVInLine
from clotureinline import ClotureInLine
from greta.administration.models import LettreCommande, Rdv, Marche, ChargeInsertion, Bilan, models_etat
from greta.administration.pdf.base_evenement import evenementBase
from greta.administration.pdf.bilanPdf import bilanDoc
from greta.administration.pdf.facture import FactureDoc
from greta.administration.csv import csvResponse
from greta.administration import params
import myfields
from datetime import timedelta 
import pdb

class LettreCommandeForm(forms.ModelForm):
    class Meta:
        model = LettreCommande
        
    date_debut = myfields.MyDateField(required=True, label=u"Date de début (jj/mm/aaaa)")
    date_fin = myfields.MyDateField(required=True, label=u"Date de fin (jj/mm/aaaa)")
    
    def clean_numero_lc(self):
        data = self.cleaned_data['numero_lc']
        if data == '':
            return None
        return data
    
    def clean(self):
        super(LettreCommandeForm, self).clean()
        if self.is_valid():
            date_debut = self.cleaned_data.get('date_debut')
            date_fin = self.cleaned_data.get('date_fin')
            if date_fin-date_debut != timedelta(days=(params.duree_lc - 1)):
                raise forms.ValidationError(u"La durée de la lettre de commande n'est pas de " + str(params.duree_lc) + u" jours")
        return self.cleaned_data
    
    
class querySetValidator(object):
    
    def __init__(self, queryset):
        self.queryset = queryset
        
    def onePopulated(self):
        if len(self.queryset) > 1:
            return (False, u"Veuillez sélectionner une seule lettre de commande")
        return (True, '')
        
    def oneNotEnAttente(self):
        (bool, msg) = self.onePopulated()
        if bool:
            lc = self.queryset.get()
            if lc.avancement!=models_etat.LC_EN_ATTENTE:
                return (True, '')
            return (False, u"La lettre de commande sélectionnée est en attente")
        return (bool, msg) 
        
    def oneAbandonnee(self):
        (bool, msg) = self.onePopulated()
        if bool:
            lc = self.queryset.get()
            if lc.abandon:
                return (True, '')
            return (False, u"La lettre de commande sélectionnée n'est pas abandonnée")
        return (bool, msg)
    
    def oneEntreEnPresta(self):
        (bool, msg) = self.onePopulated()
        if bool:
            lc = self.queryset.get()
            if lc.entreEnPresta():
                return (True, '')
            return (False, u"Le bénéficiaire n'est pas entré en prestation")
        return (bool, msg)
    
    def oneCloture(self):
        (bool, msg) = self.onePopulated()
        if bool:
            lc = self.queryset.get()
            if lc.avancement == models_etat.LC_CLOTURE:
                return (True, '')
            return (False, u"La lettre de commande n'est pas cloturée")
        return (bool, msg)
            
class lettreCommandeAdmin(admin.ModelAdmin):

    form = LettreCommandeForm
    
    inlines = [ouvertureRdvInLine, EtatCivilInline, SituationSocioProInLine, FreinInLine, CVInLine, rdvInLine, bilanInLine, ClotureInLine]
    exclude = ['avancement', 'abandon']
    list_display = ['friendly_numlc', 'format_debut', 'format_fin', 'format_polemploi_id', 'nom', 'prenom', 'avancement', 'dernier_jour_presta', 'abandon', 'site']
    list_display_links = ('friendly_numlc', 'nom')
    list_filter = ['date_debut', 'date_fin', 'avancement', 'abandon', 'site', 'charge_insertion']
    search_fields = ['nom', 'prenom', 'numero_lc', 'polemploi_id']
    date_hierarchy = 'date_debut'
    ordering = ['nom',]
    actions = ['fiche_evenement_ouverture_est', 'fiche_evenement_ouverture_sud_est', 'fiche_evenement_abandon_est', 'fiche_evenement_abandon_sud_est', 'facture_csv', 'bilan', 'facturation']
    save_on_top = True
    

    def queryset(self, request):
        if request.user.has_perm('administration.add_lettrecommande'):
            if request.user.groups.filter(name=u"Chargés d'insertion"):
                return LettreCommande.objects.filter(charge_insertion__prenom__icontains=request.user.first_name.strip()).filter(charge_insertion__nom__icontains=request.user.last_name.strip())
            return LettreCommande.objects.all()
        return None 
                 
    def get_actions(self, request):
        actions = super(lettreCommandeAdmin, self).get_actions(request)
        try:
            request.user.groups.get(name='Charge Insertion')
            del actions['facturation']
            del actions['facture_csv']
            return actions
        except ObjectDoesNotExist:
            pass
        return actions   
    
    
    def checks_evenement(self, request, queryset, typeEvenement):
        validator = querySetValidator(queryset)
        if typeEvenement == evenementBase.DEBUT:
            return validator.oneNotEnAttente()
        else: #typeEvenement == evenementBase.ABABNDON    
            return validator. oneAbandonnee()
    
    def fiche_evenement(self, request, queryset, zone, typeEvenement):
        (bool, msg) = self.checks_evenement(request, queryset, typeEvenement)
        if bool:
            lc = queryset.get()
            response = HttpResponse(mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=fiche_evenement_'+lc.numero_lc+'.pdf'
            even = evenementBase(response,lc)
            even.buildDoc(zone=zone, typeEvenement=typeEvenement)
            return response
        self.message_user(request, msg)
            
    def fiche_evenement_ouverture_est(self, request, queryset):
        return self.fiche_evenement(request, queryset, zone=evenementBase.EST, typeEvenement=evenementBase.DEBUT)
    fiche_evenement_ouverture_est.short_description = u"Fiche évènement début de prestation EST"
    
    def fiche_evenement_ouverture_sud_est(self, request, queryset):
        return self.fiche_evenement(request, queryset, zone=evenementBase.SUD_EST, typeEvenement=evenementBase.DEBUT)
    fiche_evenement_ouverture_sud_est.short_description = u"Fiche évènement début de prestation SUD-EST"
    
    def fiche_evenement_abandon_est(self, request, queryset):
        return self.fiche_evenement(request, queryset, zone=evenementBase.EST, typeEvenement=evenementBase.ABANDON)
    fiche_evenement_abandon_est.short_description = u"Fiche évènement abandon de prestation EST"
    
    def fiche_evenement_abandon_sud_est(self, request, queryset):
        return self.fiche_evenement(request, queryset, zone=evenementBase.SUD_EST, typeEvenement=evenementBase.ABANDON)
    fiche_evenement_abandon_sud_est.short_description = u"Fiche évènement abandon de prestation SUD-EST"
    
    def facture_csv(self, request, queryset):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=previsions.xls'
        return csvResponse.writeResponse(request, queryset, response)
    facture_csv.short_description = u"Prévisions de facturation"
    
    def bilan(self, request, queryset):
        (bool, msg) = querySetValidator(queryset).oneEntreEnPresta()
        if bool:
            lc = queryset.get()
            response = HttpResponse(mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=bilan_'+lc.numero_lc+'.pdf'
            bilanDoc(response, lc).buildDoc()
            return response
        self.message_user(request, msg)
    bilan.short_description = u"Bilan de prestation"
        
    def facturation(self, request, queryset):
        (bool, msg) = querySetValidator(queryset).oneCloture()
        if bool:
            lc = queryset.get()
            response = HttpResponse(mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=facture_'+lc.numero_lc+'.pdf'
            FactureDoc(response, lc).buildDoc()
            return response
        self.message_user(request, msg)
    facturation.short_description = u"Facturation"
                     
        
admin.site.disable_action('delete_selected')       
admin.site.register(LettreCommande,lettreCommandeAdmin)
admin.site.register(Marche)

