# -*- coding: utf-8 -*-
from django.db import models
from prestataire import Prestataire
import models_etat
#from lettrecommande import LettreCommande

class Site(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Site"
        verbose_name_plural = u"Sites"
        ordering = ['nom']

    def __unicode__(self):
        return "%s" % (self.nom,)

    prestataire = models.ForeignKey(Prestataire)
    nom = models.CharField(u"Nom du site", max_length=50)
    adresse = models.TextField(u"Adresse",null=True, blank=True)
    codepostal = models.CharField(u"Code postal", max_length=50, null=True, blank=True)
    ville = models.CharField(u"Ville", max_length=50, null=True, blank=True)
    telephone = models.CharField(u"Téléphone", max_length=50, null=True, blank=True)

    def lc_stats(self):
        nb_en_attente = self.lettrecommande_set.filter(avancement__exact=models_etat.LC_EN_ATTENTE).count()
        nb_en_cours = self.lettrecommande_set.filter(avancement__exact=models_etat.LC_EN_COURS).count()
        nb_cloture = self.lettrecommande_set.filter(avancement__exact=models_etat.LC_CLOTURE).count()
        return {models_etat.LC_EN_ATTENTE: nb_en_attente,\
                models_etat.LC_EN_COURS: nb_en_cours,\
                models_etat.LC_CLOTURE: nb_cloture}
        
