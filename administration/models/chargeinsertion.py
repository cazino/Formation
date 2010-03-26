# -*- coding: utf-8 -*-
from django.db import models
from site import Site
import  models_etat

class ChargeInsertion(models.Model):

    class Meta:
        app_label = 'administration'
        verbose_name = "Chargé d'insertion"
        verbose_name_plural = "Chargés d'insertion"
        ordering = ['nom']


    les_sites = models.ManyToManyField('Site')
   
    nom = models.CharField(u"Nom", max_length=50)
    prenom = models.CharField(u"Prénom", max_length=50)
    tel_fixe = models.CharField(u"Téléphone fixe", max_length=50, null=True, blank=True)
    tel_mobile = models.CharField(u"Téléphone mobile", max_length=50, null=True, blank=True)
    tel_fax = models.CharField(u"Fax", max_length=50, null=True, blank=True)
    mail = models.EmailField(u"Email", null=True, blank=True)
    
    def __unicode__(self):
        return "%s %s" % (self.nom,self.prenom)
       
    def lc_actif(self):
        return sum([1 for lc in self.lettrecommande_set.all() if lc.avancement == models_etat.LC_EN_COURS])
    lc_actif.short_description = u"Lettres de commande actives"
    
    def lc_attente(self):
        return sum([1 for lc in self.lettrecommande_set.all() if lc.avancement == models_etat.LC_EN_ATTENTE])
    lc_attente.short_description = u"Lettres de commande en attente"
    
    def lesSites(self):
        return ','.join([site.nom for site in self.les_sites.all()])
    lesSites.short_description = u"Sites"
