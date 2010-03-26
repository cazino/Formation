# -*- coding: utf-8 -*-
from django.db import models
from lettrecommande import LettreCommande



class Formation(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Formation"
        verbose_name_plural = u"Formation"

    def __unicode__(self):
        return "%s %s" % (self.lettre_commande.nom, self.lettre_commande.prenom)

    # Bénéficiaire
    lettre_commande = models.OneToOneField('LettreCommande')

     # Mobilite
    NIVEAU_CHOIX = (
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
        ('VI', 'VI'),
    )

    PRESTA_CHOIX = (
        ('Bilan de compétences', 'Bilan de compétences'),
        ('VAE', 'VAE'),
        ('Formation Pôle-emploi/Etat', 'Formation Pôle-emploi/Etat'),
        ('Formation CRIF', 'Formation CRIF'),
        ('Formation C.Général', 'Formation C.Général')
    )
    

    besoin = models.NullBooleanField("Besoin d'une formation ?", null=True, blank=True)
    niveau = models.CharField("Niveau ?", max_length=3, choices=NIVEAU_CHOIX, null=True, blank=True)
    formationtype = models.TextField("Quel formation et quel organisme ?", null=True, blank=True)
    qualifiante = models.NullBooleanField("Formation qualifiante ?", null=True, blank=True)
    certifiante = models.NullBooleanField("Formation certifiante ?", null=True, blank=True)
    stage = models.NullBooleanField("Envoyé en stage ?", null=True, blank=True)
    formasend = models.NullBooleanField("Envoyé à faire une formation ?", null=True, blank=True)
    departement = models.TextField("Dans le département ?", null=True, blank=True)
    presta = models.CharField("Type de prestation ?", max_length=50, choices=PRESTA_CHOIX, null=True, blank=True)
    
    
