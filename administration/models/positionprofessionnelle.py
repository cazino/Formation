# -*- coding: utf-8 -*-
from django.db import models
from lettrecommande import LettreCommande



class PositionProfessionnelle(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Position professionnelle"
        verbose_name_plural = u"Position professionnelle"

    def __unicode__(self):
        return "%s %s" % (self.lettre_commande.nom, self.lettre_commande.prenom)

    # Bénéficiaire
    lettre_commande = models.OneToOneField('LettreCommande')

     # Mobilite
    QUALIF_CHOIX = (
        ('Sans', 'Sans'),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
        ('VI', 'VI'),
    )

    CONTRAT_CHOIX = (
        ('CDD', 'CDD'),
        ('CDI', 'CDI'),
        ('Autre', 'Autre'),
    )

    COUT_CHOIX = (
        ('Positif', 'Positif'),
        ('Négatif', 'Négatif'),
    )
    
    metier1 = models.TextField("Métier 1 ?", null=True, blank=True)
    contrat1 = models.CharField("Type de contrat ?", max_length=3, choices=CONTRAT_CHOIX, null=True, blank=True)
    dureemois1 = models.IntegerField("Durée (mois)", null=True, blank=True)
    dureean1 = models.IntegerField("Durée (années)", null=True, blank=True)
    #secteur1 = 

    metier2 = models.TextField("Métier 2 ?", null=True, blank=True)
    contrat2 = models.CharField("Type de contrat ?", max_length=3, choices=CONTRAT_CHOIX, null=True, blank=True)
    dureemois2 = models.IntegerField("Durée (mois)", null=True, blank=True)
    dureean2 = models.IntegerField("Durée (années)", null=True, blank=True)

    metier3 = models.TextField("Métier 3 ?", null=True, blank=True)
    contrat3 = models.CharField("Type de contrat ?", max_length=3, choices=CONTRAT_CHOIX, null=True, blank=True)
    dureemois3 = models.IntegerField("Durée (mois)", null=True, blank=True)
    dureean3 = models.IntegerField("Durée (années)", null=True, blank=True)


    qualif = models.CharField("Niveau de qualification ?", max_length=4, choices=QUALIF_CHOIX, null=True, blank=True)
    cv = models.NullBooleanField("CV actualisé ?", null=True, blank=True)
    motiv = models.NullBooleanField("Lettre de motication ?", null=True, blank=True)
    polemp = models.NullBooleanField("Consultez-vous pôle emploi ?", null=True, blank=True)
    web = models.NullBooleanField("Allez-vous sur internet ?", null=True, blank=True)
    web_polemp = models.NullBooleanField("Allez-vous sur pole-emploi.fr ?", null=True, blank=True)
    web_autre = models.NullBooleanField("Allez-vous sur d'autres sites d'emploi ?", null=True, blank=True)
    web_detail = models.TextField("Si oui lesquels ?", null=True, blank=True)
    reseau = models.NullBooleanField("Entretenez-vous un réseau pro ?", null=True, blank=True)
    entretien = models.NullBooleanField("Avez-vous des entretiens ?", null=True, blank=True)
    secteurporteur = models.NullBooleanField("Y-a-t-il du travail dans le secteur visé ?", null=True, blank=True)
    pbmobilite = models.NullBooleanField("Problèmes de mobilité-transport ?", null=True, blank=True)
    pbage = models.NullBooleanField("Problème de l'âge ?", null=True, blank=True)
    pbqualif = models.NullBooleanField("Problème de qualification ?", null=True, blank=True)
    tafproxi = models.NullBooleanField("Pensez-vous retravailler près de chez vous ?", null=True, blank=True)
    handicap = models.NullBooleanField("Avez-vous un handicap ?", null=True, blank=True)
    gardenf = models.NullBooleanField("Problème de garde d'anfants ?", null=True, blank=True)
    cout = models.CharField("Coût garde+transport / travail ?", choices=COUT_CHOIX, max_length=7,null=True, blank=True)
    
    



