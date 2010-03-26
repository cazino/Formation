# -*- coding: utf-8 -*-
from django.db import models
from lettrecommande import LettreCommande



class Intervention(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Intervention"
        verbose_name_plural = u"Intervention"


    def __unicode__(self):
        return "%s %s" % (self.lettre_commande.nom, self.lettre_commande.prenom)

    SUJET_CHOIX = (
        ('Logement', 'Logement'),
        ('Social', 'Social'),
        ('Santé', 'Santé'),
        ('Justice', 'Justice')
    )

    CONTRAT_CHOIX = (
        ('Oui', 'Oui'),
        ('Non', 'Non'),
        ('RSA en cours', 'RSA en cours')
    )

    SUIVI_CHOIX = (
        ('DDASMA', 'DDASMA'),
        ('REALITE', 'REALITE'),
        ('Pôle emploi', 'Pôle emploi'),
        ('PROMETHEE', 'PROMETHEE'),
        ('Mission locale', 'Mission locale'),
        ('Autre', 'Autre')
    )

    #Bénéficiaire
    lettre_commande = models.OneToOneField('LettreCommande')

    exist = models.NullBooleanField("Bénificiez vous d'une intervention ?", null=True, blank=True)
    sujet = models.CharField("Bénificiez vous d'une intervention ?", max_length=8, choices=SUJET_CHOIX, null=True, blank=True)
    logement = models.NullBooleanField("Avez-vous un logement stable ?", null=True, blank=True)
    demenagement = models.NullBooleanField("Envisagez-vous de déménager ?", null=True, blank=True)
    tribunaux = models.NullBooleanField("Réglez-vous actuellement des problèmes devant les tribunaux ?", null=True, blank=True)
    tuteur = models.NullBooleanField("Avez-vous un tuteur/curateur ?", null=True, blank=True)
    contact_tuteur = models.TextField("Contact tuteur/curateur", null=True, blank=True)
    contrat_insertion = models.CharField("Avez-vous signé un contrat d'insertion ?", choices=CONTRAT_CHOIX, max_length=20, null=True, blank=True)
    suivi = models.CharField("Bénificiez-vous d'un suivi ?", choices=CONTRAT_CHOIX, max_length=20, null=True, blank=True)
    suivi_autre = models.TextField("Si autre qui ?", null=True, blank=True)
    suivi_referent = models.TextField("Quel est votre référent ou la personne qui vous suit ?", null=True, blank=True)


