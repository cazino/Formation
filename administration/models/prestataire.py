# -*- coding: utf-8 -*-
from django.db import models
import models_etat 

class Prestataire(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Prestataire"
        verbose_name_plural = u"Prestataires"
        ordering = ['nom']

    def __unicode__(self):
        return "%s" % (self.nom,)

    
    nom = models.CharField(u"Nom du prestataire", max_length=50)

    cfc_nom = models.CharField(u"Nom", max_length=50, null=True, blank=True)
    cfc_prenom = models.CharField(u"Prénom", max_length=50, null=True, blank=True)
    cfc_telfixe = models.CharField(u"Téléphone fixe", max_length=50, null=True, blank=True)
    cfc_telmobile = models.CharField(u"Téléphone mobile", max_length=50, null=True, blank=True)
    cfc_fax = models.CharField(u"Fax", max_length=50, null=True, blank=True)
    cfc_mail = models.EmailField(u"Email", null=True, blank=True)

    caf_nom = models.CharField(u"Nom", max_length=50, null=True, blank=True)
    caf_prenom = models.CharField(u"Prénom", max_length=50, null=True, blank=True)
    caf_telfixe = models.CharField(u"Téléphone fixe", max_length=50, null=True, blank=True)
    caf_telmobile = models.CharField(u"Téléphone mobile", max_length=50, null=True, blank=True)
    caf_fax = models.CharField(u"Fax", max_length=50, null=True, blank=True)
    caf_mail = models.EmailField(u"Email", null=True, blank=True)
    
    coor_nom = models.CharField(u"Nom", max_length=50, null=True, blank=True)
    coor_prenom = models.CharField(u"Prénom", max_length=50, null=True, blank=True)
    coor_telfixe = models.CharField(u"Téléphone fixe", max_length=50, null=True, blank=True)
    coor_telmobile = models.CharField(u"Téléphone mobile", max_length=50, null=True, blank=True)
    coor_fax = models.CharField(u"Fax", max_length=50, null=True, blank=True)
    coor_mail = models.EmailField(u"Email", null=True, blank=True)
    
    def lc_stats(self):
        les_sites_stats = [oneSite.lc_stats() for oneSite in self.site_set.all()]
        nb_en_attente = sum([statdic[models_etat.LC_EN_ATTENTE] for statdic in les_sites_stats])
        nb_en_cours = sum([statdic[models_etat.LC_EN_COURS] for statdic in les_sites_stats])
        nb_cloture = sum([statdic[models_etat.LC_CLOTURE] for statdic in les_sites_stats])
        return {models_etat.LC_EN_ATTENTE: nb_en_attente, models_etat.LC_EN_COURS: nb_en_cours, models_etat.LC_CLOTURE: nb_cloture}
         
        
        
