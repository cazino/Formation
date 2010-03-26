# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals
#from django.dispatch import dispatcher
from marche import Marche
from site import Site
from prestataire import Prestataire
from chargeinsertion import ChargeInsertion
from ouverturerdv import ouvertureRdv
from models_etat import *
import pdb

class LettreCommande(models.Model):

    class Meta:
        app_label = 'administration'
        verbose_name = "Lettre de commande"
        verbose_name_plural = "Lettres de commandes"

       
    # TYPE DE PRESTATION
    BCA = u"BCA"
    CIBLE = u"CIBLE"
    OP_CREA = u"OP CREA" 
    ECCP = u"ECCP"
    MOB = u"MOB"
    STR = u"STR"
    EPCE = u"EPCE"
    AUTRE = u"AUTRE"
    TYPES_PRESTA = ((BCA, BCA),
                    (CIBLE, CIBLE),
                    (OP_CREA, OP_CREA),
                    (ECCP, ECCP),
                    (MOB, MOB),
                    (STR,STR),
                    (MOB, MOB),
                    (STR, STR),
                    (EPCE, EPCE),
                    (AUTRE,AUTRE),
                    )
    
    CIVILITE = ((1, 'Homme'),
                ( 2, 'Femme')
                )
    
    MVE = (('MVEG', 'MVEG'),
           ('MVEP', 'MVEP'))
    
    marche = models.ForeignKey(Marche)
    charge_insertion = models.ForeignKey(ChargeInsertion)
    site = models.ForeignKey(Site)
    mv = models.CharField(u"MVEG ou MVEP", choices=MVE, default=MVE[0][0], max_length=4)
    numero_lc = models.SlugField(u"Numéro", null=True, blank=True, max_length=50, unique=True)
    date_debut = models.DateField(u"Début")
    date_fin = models.DateField(u"Fin")
    civilite = models.PositiveIntegerField(u"Civilite", choices=CIVILITE, default=1)
    nom = models.CharField(u"Nom", max_length=50)
    prenom = models.CharField(u"Prénom", max_length=50)
    polemploi_id = models.SlugField(u"Identifiant pôle emploi du bénéficaire", max_length=50)
    ale_prescriptrice = models.CharField(u"ALE prescriptrice", max_length=100)
    conseiller_ploleemploi = models.CharField(u"Conseiller pôle emploi", max_length=100)
    type_presta = models.CharField(u"Type de prestation", choices=TYPES_PRESTA, null=True, blank=True, max_length=10)
    typePresta_autre = models.CharField(u"Si AUTRE, précisez", null=True, blank=True, max_length=200)
    
    # Pseudo-calculated fields
    avancement = models.CharField(u"Avancement",max_length=20, default=LC_EN_ATTENTE)
    abandon = models.BooleanField(u"Abandon", default=False)
     
    def __unicode__(self):
        return "%s %s" % (self.numero_lc, self.nom)
    
    def format_debut(self):
        return self.date_debut.strftime("%d/%m/%Y")
    format_debut.admin_order_field = 'date_debut'
    format_debut.short_description = u"Début"
    
    def format_fin(self):
        return self.date_fin.strftime("%d/%m/%Y")
    format_fin.admin_order_field = 'date_fin'
    format_fin.short_description = u"Fin"
    
    def format_polemploi_id(self):
        return self.polemploi_id
    format_polemploi_id.admin_order_field = 'polemploi_id'
    format_polemploi_id.short_description = u"Identifiant"
    
    def beneficiaireNom(self):
        return self.nom
    beneficiaireNom.short_description = 'Bénéficiaire'

    def changeAvancement(self,nouvelAvancement):
        self.avancement = nouvelAvancement
        self.save()
    
    def notifyOuvertureSave(self,ouverture_rdv):
        rdv_statut = ouverture_rdv.statut
        if rdv_statut == ouvertureRdv.ABSENT or rdv_statut == ouvertureRdv.REPORT or rdv_statut == ouvertureRdv.PRESENT_NC:
            self.abandon=False
            self.changeAvancement(LC_ANNULE)
        elif ouverture_rdv.statut == ouvertureRdv.PRESENT_C:
            self.abandon=False
            self.changeAvancement(LC_EN_COURS)    

    def notifyOuvertureDelete(self,ouverture_rdv):
        self.changeAvancement(LC_EN_ATTENTE)

    def notifyClotureSave(self,cloture_rdv):
        if self.avancement == LC_EN_COURS or self.avancement == LC_CLOTURE:
            if cloture_rdv.terme:
                self.abandon=False
            else:
                self.abandon=True
            self.changeAvancement(LC_CLOTURE)
            
    def notifyClotureDelete(self,cloture_rdv):
        if self.avancement==LC_CLOTURE:
            self.abandon=False
            self.changeAvancement(LC_EN_COURS)
            
    def lastRdv(self):
        try:
            rdv_queryset = self.rdv.exclude(typerdv__exact=RDV_HEBDO) 
            if rdv_queryset.count():
                return rdv_queryset.latest('dateheure') 
            if self.ouverture_rdv:
                return self.ouverture_rdv
        except ObjectDoesNotExist:
            return None
    
    def lastRdvDate(self):
        lastRdv = self.lastRdv()
        if lastRdv:
            return lastRdv.dateheure.date()
        return None
    
    def lastDayPresta(self):
        if self.avancement==LC_CLOTURE:
            if self.abandon:
                return self.cloture.date_abandon
            return self.date_fin
        return None
    
    def dernier_jour_presta(self):
        ldp = self.lastDayPresta() 
        if ldp:
            return ldp.strftime("%d/%m/%Y")
        return ''
    dernier_jour_presta.short_description = u"Dernier jour de prestation" 
    
    def entreEnPresta(self):
        return self.avancement==LC_EN_COURS or self.avancement==LC_CLOTURE

    def friendly_numlc(self):
        if not self.numero_lc:
            return ''
        return self.numero_lc
    friendly_numlc.admin_order_field = 'numero_lc'
    friendly_numlc.short_description = u"Numéro"
    

