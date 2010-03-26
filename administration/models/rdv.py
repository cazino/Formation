# -*- coding: utf-8 -*-
from django.db import models
import models_etat

class Rdv(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Rendez-vous de suivi"
        verbose_name_plural = u"Rendez-vous de suivi"


    def __unicode__(self):
        return "%s - %s" % (self.typerdv, self.dateheure.strftime("%d/%m/%Y"))


    
    RDV_CHOIX = ((models_etat.RDV_HEBDO, models_etat.RDV_HEBDO),
                 (models_etat.RDV_IND, models_etat.RDV_IND),
                 (models_etat.RDV_THEM, models_etat.RDV_THEM))




    lettre_commande = models.ForeignKey('LettreCommande', related_name='rdv')
    dateheure = models.DateTimeField("Date et heure")
    present = models.BooleanField("Bénéficiaire présent")
    typerdv = models.CharField("Type de rendez-vous", max_length=50, choices=RDV_CHOIX)
    
    # Accompagnement social
    accsoc_date1 = models.CharField(u"Date 1", max_length=100, null=True, blank=True)
    accsoc_insti1 = models.TextField(u"Institutions-organismes sollicités 1", null=True, blank=True)
    accsoc_action1 = models.TextField(u"Actions réalisées 1", null=True, blank=True)
    accsoc_results1 = models.TextField(u"Résultats 1", null=True, blank=True)
    
    accsoc_date2 = models.CharField(u"Date 2", max_length=100, null=True, blank=True)
    accsoc_insti2 = models.TextField(u"Institutions-organismes sollicités 2", null=True, blank=True)
    accsoc_action2 = models.TextField(u"Actions réalisées 2", null=True, blank=True)
    accsoc_results2 = models.TextField(u"Résultats 2", null=True, blank=True)
    
    accsoc_date3 = models.CharField(u"Date 3", max_length=100, null=True, blank=True)
    accsoc_insti3 = models.TextField(u"Institutions-organismes sollicités 3", null=True, blank=True)
    accsoc_action3 = models.TextField(u"Actions réalisées 3", null=True, blank=True)
    accsoc_results3 = models.TextField(u"Résultats 3", null=True, blank=True)
    
    accsoc_date4 = models.CharField(u"Date 4", max_length=100, null=True, blank=True)
    accsoc_insti4 = models.TextField(u"Institutions-organismes sollicités 4", null=True, blank=True)
    accsoc_action4 = models.TextField(u"Actions réalisées 4", null=True, blank=True)
    accsoc_results4 = models.TextField(u"Résultats 4", null=True, blank=True)
    
    
    # Accompagnement emploi
    accemp_date1 = models.CharField(u"Date 1", max_length=100, null=True, blank=True)
    accemp_entr1 = models.TextField(u"Entreprises contactées 1", null=True, blank=True)
    accemp_mod1 = models.TextField(u"Modalités 1", null=True, blank=True)
    accemp_results1 = models.TextField(u"Résultats 1", null=True, blank=True)
    
    accemp_date2 = models.CharField(u"Date 2", max_length=100, null=True, blank=True)
    accemp_entr2 = models.TextField(u"Entreprises contactées 2", null=True, blank=True)
    accemp_mod2 = models.TextField(u"Modalités 2", null=True, blank=True)
    accemp_results2 = models.TextField(u"Résultats 2", null=True, blank=True)
    
    accemp_date3 = models.CharField(u"Date 3", max_length=100, null=True, blank=True)
    accemp_entr3 = models.TextField(u"Entreprises contactées 3", null=True, blank=True)
    accemp_mod3 = models.TextField(u"Modalités 3", null=True, blank=True)
    accemp_results3 = models.TextField(u"Résultats 3", null=True, blank=True)
    
    accemp_date4 = models.CharField(u"Date 4", max_length=100, null=True, blank=True)
    accemp_entr4 = models.TextField(u"Entreprises contactées 4", null=True, blank=True)
    accemp_mod4 = models.TextField(u"Modalités 4", null=True, blank=True)
    accemp_results4 = models.TextField(u"Résultats 4", null=True, blank=True)
    
    #Parcours proposé
    parcours = models.TextField(u"Parcours proposé", null=True, blank=True)
    

    
