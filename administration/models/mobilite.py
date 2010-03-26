# -*- coding: utf-8 -*-
from django.db import models
from lettrecommande import LettreCommande



class Mobilite(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Mobilité"
        verbose_name_plural = u"Mobilité"

    def __unicode__(self):
        return "%s %s" % (self.lettre_commande.nom, self.lettre_commande.prenom)

    #Bénéficiaire
    lettre_commande = models.OneToOneField('LettreCommande')

     # Mobilite
    PERMIS_CHOIX = (
        ('A', 'A'),
        ('A1', 'A1'),
        ('B', 'B'),
        ('B1', 'B1'),
        ('C', 'C'),
        ('D', 'D'),
        ('Eb', 'Eb'),
        ('Ec', 'Ec'),
        ('Ed', 'Ed')
    )
    permis = models.CharField("Quel permis possédez vous ?", max_length=2, choices=PERMIS_CHOIX, null=True, blank=True)
    inscrit_permis = models.NullBooleanField("Etes-vous inscrit au permis ?", null=True, blank=True)
    aide_permis = models.NullBooleanField("Avez vous besoin d'aide au permis ?", null=True, blank=True)
    vehicule = models.NullBooleanField("Avez vous un véhicule ?", null=True, blank=True)
    vehicule_limite = models.NullBooleanField("Avez vous des limites à utiliser ce véhicule ?", null=True, blank=True)
    rayon_action = models.IntegerField("Rayon d'action (en KM)", null=True, blank=True)
    autre_transport = models.TextField("Avez-vous un autre moyen de transport ?", null=True, blank=True)

