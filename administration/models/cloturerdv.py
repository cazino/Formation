# -*- coding: utf-8 -*-
from rdv import Rdv
from django.db import models

class clotureRdv(models.Model):

    
    class Meta:
        app_label = 'administration' 
        verbose_name = u"Rdv de clôture"
        verbose_name_plural = u"Rdv clôture"

    
    lc = models.OneToOneField('LettreCommande')
    dateheure = models.DateTimeField("Date et heure")
    

    def __unicode__(self):
        return "%s" % (self.statut)
    
    def save(self, force_insert=False, force_update=False):
        super(clotureRdv, self).save(force_insert, force_update)
        self.lc.notifyClotureSave(self)

    def delete(self):
        super(clotureRdv, self).delete()
        self.lc.notifyClotureDelete(self)
        
        
