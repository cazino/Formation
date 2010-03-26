# -*- coding: utf-8 -*-
from django.db import models
#from site import Site


class Statistique(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Statistiques"
        verbose_name_plural = u"Statistiques"

    def __unicode__(self):
        return "%s %s %s %s" % (self.nom, self.site, self.debut.strftime('%d/%m/%Y'), self.fin.strftime('%d/%m/%Y'))
    
    nom = models.CharField(u"Nom", max_length=100)
    site = models.ForeignKey('Site', unique=True)
    debut = models.DateField()
    fin = models.DateField()
    
    