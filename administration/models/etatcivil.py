# -*- coding: utf-8 -*-
from django.db import models
from lettrecommande import LettreCommande
import datetime


class EtatCivil(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = "Etat civil"
        verbose_name_plural = "Etat civil"


    lettre_commande = models.OneToOneField('LettreCommande', related_name='etat_civil')
    date_naissance = models.DateField(u"Date de naissance", null=True, blank=True)
    age = models.PositiveIntegerField(u"Age", null=True, blank=True)
    lieu_naissance = models.CharField(u"Lieu de naissance", max_length=50, null=True,blank=True)
    adresse = models.TextField(u"Adresse", null=True,blank=True)
    code_postal = models.SlugField(u"Code postal", null=True,blank=True)
    ville = models.CharField(u"Ville", max_length=50, null=True,blank=True)
    telfixe = models.CharField(u"Téléphone fixe", max_length=50, null=True, blank=True)
    telmobile = models.CharField(u"Téléphone mobile", max_length=50, null=True, blank=True)
    mail = models.EmailField(u"Email", null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.lettre_commande.nom, self.lettre_commande.prenom)

    """
    def age(self):
        if self.date_naissance:
            return (datetime.date.today()-self.date_naissance)
        else:
            return '' 
    """

   
