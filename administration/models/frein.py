# -*- coding: utf-8 -*-
from django.db import models
from lettrecommande import LettreCommande



class Frein(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Frein"
        verbose_name_plural = u"Freins"
        
    def __unicode__(self):
        return "Les Freins" 

    lettre_commande = models.OneToOneField('LettreCommande', related_name='frein')

    # Freins professionnels
    PRO_INTIT = u"Freins professionnels"
    
    PRO_QUALIF = u"Qualification"
    PRO_ETU = u"Niveau d'étude"
    PRO_EXPE = u"Expérience"
    PRO_LANG = u"Langue"
    PRO_PP = u"Projet professionnel"
    PRO_CHOIX = ((PRO_QUALIF, PRO_QUALIF),
                 (PRO_ETU, PRO_ETU),
                 (PRO_EXPE, PRO_EXPE),
                 (PRO_LANG, PRO_LANG),
                 (PRO_PP, PRO_PP))
    pro1 = models.CharField(u"Premier choix", max_length=30, choices=PRO_CHOIX, null=True, blank=True)
    pro2 = models.CharField(u"Deuxième choix", max_length=30, choices=PRO_CHOIX, null=True, blank=True)
    pro3 = models.CharField(u"Troisième choix", max_length=30, choices=PRO_CHOIX, null=True, blank=True)
    
    # Freins personnels
    PERSO_INTIT = u"Freins personnels"
    
    PERSO_SANTE = u"Santé"
    PERSO_STATUT = u"Statut"
    PERSO_ENF = u"Garde d'enfant"
    PERSO_AUTO = u"Autonomie"
    PERSO_RELATIONNEL = u"Relationnel"
    PERSO_MOBILITE = u"Mobilité"
    PERSO_CHOIX = ((PERSO_SANTE, PERSO_SANTE),
                   (PERSO_STATUT, PERSO_STATUT),
                   (PERSO_ENF, PERSO_ENF),
                   (PERSO_AUTO, PERSO_AUTO),
                   (PERSO_RELATIONNEL, PERSO_RELATIONNEL),
                   (PERSO_MOBILITE, PERSO_MOBILITE))
    perso1 = models.CharField(u"Premier choix", max_length=30, choices=PERSO_CHOIX, null=True, blank=True)
    perso2 = models.CharField(u"Deuxième choix", max_length=30, choices=PERSO_CHOIX, null=True, blank=True)
    perso3 = models.CharField(u"Troisième choix", max_length=30, choices=PERSO_CHOIX, null=True, blank=True)
    
    # Freins sociaux
    SOCIO_INTIT = u"Freins sociaux"
    
    SOCIO_LOGEMENT = u"Logement"
    SOCIO_FAMILLE = u"Situation familiale"
    SOCIO_AGE = u"Age"
    SOCIO_DEPENSE = u"Dépenses et charges"
    SOCIO_DISCRI = u"Discrimination"
    SOCIO_CHOIX = ((SOCIO_LOGEMENT, SOCIO_LOGEMENT),
                   (SOCIO_FAMILLE, SOCIO_FAMILLE),
                   (SOCIO_AGE, SOCIO_AGE),
                   (SOCIO_DEPENSE, SOCIO_DEPENSE),
                   (SOCIO_DISCRI, SOCIO_DISCRI))
    socio1 = models.CharField(u"Premier choix", max_length=30, choices=SOCIO_CHOIX, null=True, blank=True)
    socio2 = models.CharField(u"Deuxième choix", max_length=30, choices=SOCIO_CHOIX, null=True, blank=True)
    socio3 = models.CharField(u"Troisième choix", max_length=30, choices=SOCIO_CHOIX, null=True, blank=True)
    
    # Freins emploi
    EMPL_INTIT = u"Freins emploi"
    
    EMPL_CONJ = u"Conjoncture"
    EMPL_EXI = u"Exigence"
    EMPL_REM = u"Rémunération"
    EMPL_CONC = u"Concurrence"
    EMPL_CHOIX = ((EMPL_CONJ, EMPL_CONJ),
                  (EMPL_EXI, EMPL_EXI),
                  (EMPL_REM, EMPL_REM),
                  (EMPL_CONC, EMPL_CONC))
    empl1 = models.CharField(u"Premier choix", max_length=30, choices=EMPL_CHOIX, null=True, blank=True)
    empl2 = models.CharField(u"Deuxième choix", max_length=30, choices=EMPL_CHOIX, null=True, blank=True)
    empl3 = models.CharField(u"Troisième choix", max_length=30, choices=EMPL_CHOIX, null=True, blank=True)
    
    # Autres freins
    autr = models.TextField(u"Autres freins", null=True, blank=True)
    
    nom_freins = [PRO_INTIT, PERSO_INTIT, SOCIO_INTIT, EMPL_INTIT]
    valeurs_freins = [[valeur for (valeur, valeur_bis) in PRO_CHOIX],
                      [valeur for (valeur, valeur_bis) in PERSO_CHOIX],
                      [valeur for (valeur, valeur_bis) in SOCIO_CHOIX],
                      [valeur for (valeur, valeur_bis) in EMPL_CHOIX]]
    freins_dic = dict([(nom_freins[pos], valeurs_freins[pos]) for pos in range(len(nom_freins))])

