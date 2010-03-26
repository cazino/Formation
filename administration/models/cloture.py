# -*- coding: utf-8 -*-
from django.db import models


class Cloture(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Cloture"
        verbose_name_plural = u"Cloture"

    lettre_commande = models.OneToOneField('LettreCommande', related_name='cloture')
    terme = models.BooleanField(u"Lettre de commande arrivée à son terme")
    date_abandon = models.DateField(u"Si non, abandon à la date", null=True, blank=True)
    motif = models.TextField(u"Motif de l'abandon", null=True, blank=True)
     
    def __unicode__(self):
        if not self.terme:
            return u" Abandon %s" % (self.date_abandon.strftime("%d/%m/%Y"),)
        else:
            return u"Terme"
     
    def save(self, force_insert=False, force_update=False):
        super(Cloture, self).save(force_insert, force_update)
        self.lettre_commande.notifyClotureSave(self)

    def delete(self):
        super(Cloture, self).delete()
        self.lettre_commande.notifyClotureDelete(self)
        
    
    
   
