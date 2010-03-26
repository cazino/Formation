# -*- coding: utf-8 -*-
from rdv import Rdv
from django.db import models

class ouvertureRdv(models.Model):

    
    class Meta:
        app_label = 'administration' 
        verbose_name = u"Rendez-vous d'ouverture"
        verbose_name_plural = u"Rendez-vous d'ouverture"

    ABSENT = u"Absent"
    REPORT = u"Report"
    PRESENT_NC = u"Présent non contractualisé"
    PRESENT_C = u"Présent contractualisé"

    STATUT_CHOIX = (
        (ABSENT, ABSENT),
        (REPORT, REPORT),
        (PRESENT_NC, PRESENT_NC),
        (PRESENT_C, PRESENT_C),
    )

    lettre_commande = models.OneToOneField('LettreCommande', related_name='ouverture_rdv')
    dateheure = models.DateTimeField("Date et heure")
    statut = models.CharField("Statut", max_length=50, choices=STATUT_CHOIX)
    motif = models.TextField("Si non contratualisation, indiquer le motif", null=True, blank=True)
    dateheure_nouveauRdv = models.DateTimeField("Si report, date et heure du  nouveau rendez-vous", null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.statut)
    
    def save(self, force_insert=False, force_update=False):
        super(ouvertureRdv, self).save(force_insert, force_update)
        self.lettre_commande.notifyOuvertureSave(self)

    def delete(self):
        super(ouvertureRdv, self).delete()
        self.lettre_commande.notifyOuvertureDelete(self)
        
        
        
    
    
