# -*- coding: utf-8 -*-
from django.db import models
from lettrecommande import LettreCommande

class CV(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"CV"
        verbose_name_plural = u"CV"
    
    def __unicode__(self):
        return "Les CV"  

    lettre_commande = models.OneToOneField('LettreCommande', related_name='cv')
    cv1 = models.FileField(u"Fichier", upload_to='cv', null=True, blank=True)
    cv1_description = models.CharField(u"Description", max_length=100, null=True, blank=True)
    cv2 = models.FileField(u"Fichier", upload_to='cv', null=True, blank=True)
    cv2_description = models.CharField(u"Description", max_length=100, null=True, blank=True)
    