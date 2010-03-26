# -*- coding: utf-8 -*-
from django.db import models
from lettrecommande import LettreCommande
import datetime


class SituationSocioPro(models.Model):

    class Meta:
        app_label = 'administration' 
        verbose_name = u"Situation socio-professionnelle"
    
    
    lettre_commande = models.OneToOneField('LettreCommande', related_name='situation_sociopro')
        
    #Allocation
    AL_ARE = u"ARE"
    AL_RSA = u"RSA"
    AL_ASS = u"ASS"
    AL_TTP = u"TTP"
    AL_DENI = u"DENI"
    AL_RAH = u"RAH"
    AL_CHOIX = ((AL_ARE, AL_ARE),
                (AL_RSA, AL_RSA),
                (AL_ASS, AL_ASS),
                (AL_TTP, AL_TTP),
                (AL_DENI, AL_DENI),
                (AL_RAH, AL_RAH))
    al_type = models.CharField(u"Type d'allocation", max_length=10, choices=AL_CHOIX, null=True,blank=True)
    al_date = models.DateField(u"Date de début du versement de l'allocation", null=True, blank=True)
    
    
    #Situation familiale
    SF_CELIB = u"Célibataire"
    SF_MARIE = u"Marié"
    SF_PACSE = u"Pacsé"
    SF_VM = u"Vie maritale"
    SF_VEUF = u"Veuf"  
    SF_CHOIX = ((SF_CELIB, SF_CELIB),
                (SF_MARIE, SF_MARIE),
                (SF_PACSE, SF_PACSE),
                (SF_VM, SF_VM),
                (SF_VEUF, SF_VEUF))
    sf_statut = models.CharField(u"Statut marital", max_length=15, choices=SF_CHOIX, null=True,blank=True)
    sf_nbenfants = models.PositiveIntegerField(u"Nombre d'enfants", null=True, blank=True)
    sf_modegarde =  models.TextField(u"Mode de garde", null=True,blank=True)
    
    #Projet professionnel
    pp_sansprojet = models.TextField(u"Sans projet", null=True,blank=True)
    pp_projet1 = models.TextField(u"Projet 1", null=True,blank=True)
    pp_projet2 = models.TextField(u"Projet 2", null=True,blank=True)
    
    #Mobilité
    PERMIS_A = u"A"
    PERMIS_A1 = u"A1"
    PERMIS_B = u"B"
    PERMIS_B1 = u"B1"
    PERMIS_C = u"C"
    PERMIS_Eb = u"Eb"
    PERMIS_Ec = u"Ec"
    PERMIS_Ed = u"Ed"
    PERMIS_CHOIX = ((PERMIS_A, PERMIS_A),
                    (PERMIS_A1, PERMIS_A1),
                    (PERMIS_B, PERMIS_B),
                    (PERMIS_B1, PERMIS_B1),
                    (PERMIS_C, PERMIS_C),
                    (PERMIS_Eb, PERMIS_Eb),
                    (PERMIS_Ec, PERMIS_Ec),
                    (PERMIS_Ed, PERMIS_Ed))
    mob_permis = models.CharField(u"Quel permis possédez vous ?", max_length=2, choices=PERMIS_CHOIX, null=True, blank=True)
    mob_inscritPermis = models.NullBooleanField(u"Etes-vous inscrit au permis ?", null=True, blank=True)
    mob_aidePermis = models.NullBooleanField(u"Avez vous besoin d'aide au permis ?", null=True, blank=True)
    mob_vehicule = models.NullBooleanField(u"Avez vous un véhicule ?", null=True, blank=True)
    mob_limiteVehicule = models.NullBooleanField(u"Avez vous des limites à utiliser ce véhicule ?", null=True, blank=True)
    mob_rayonAction = models.PositiveIntegerField(u"Rayon d'action (en KM)", null=True, blank=True)
    mob_autreTransport = models.CharField("Avez-vous un autre moyen de transport ?", max_length=200, null=True, blank=True)
    
    #Qualification
    NIVEAU_O = u"Sans"
    NIVEAU_I = u"I"
    NIVEAU_II = u"II"
    NIVEAU_III = u"III"
    NIVEAU_IV = u"IV"
    NIVEAU_V = u"V"
    NIVEAU_VI = u"VI"
    NIVEAU_CHOIX = ((NIVEAU_O, NIVEAU_O),
                    (NIVEAU_I, NIVEAU_I),
                    (NIVEAU_II, NIVEAU_II),
                    (NIVEAU_III, NIVEAU_III),
                    (NIVEAU_IV, NIVEAU_IV),
                    (NIVEAU_V, NIVEAU_V),
                    (NIVEAU_VI, NIVEAU_VI))
    qualif_niveau = models.CharField("Niveau de qualification", max_length=4, choices=NIVEAU_CHOIX, null=True, blank=True)
    
    #Expérience professionnelle et formation
    CONTRAT_CDI = u"CDI"
    CONTRAT_CDD = u"CDD"
    CONTRAT_AUTRE = u"Autre"
    CONTRAT_CHOIX = ((CONTRAT_CDI, CONTRAT_CDI),
                     (CONTRAT_CDD, CONTRAT_CDD),
                     (CONTRAT_AUTRE, CONTRAT_AUTRE))
    exp_expericence1 = models.TextField(u"Expérience 1", null=True, blank=True)
    exp_type1 = models.CharField("Type de contrat", max_length=5, choices=CONTRAT_CHOIX, null=True, blank=True)
    exp_duree1 = models.CharField("Durée (précisez mois ou année)", max_length=50, null=True, blank=True)
    exp_expericence2 = models.TextField(u"Expérience 2", null=True, blank=True)
    exp_type2 = models.CharField("Type de contrat", max_length=5, choices=CONTRAT_CHOIX, null=True, blank=True)
    exp_duree2 = models.CharField("Durée (précisez mois ou année)", max_length=50, null=True, blank=True)
    exp_expericence3 = models.TextField(u"Expérience 3", null=True, blank=True)
    exp_type3 = models.CharField("Type de contrat", max_length=5, choices=CONTRAT_CHOIX, null=True, blank=True)
    exp_duree3 = models.CharField("Durée (précisez mois ou année)", max_length=50, null=True, blank=True)
    
    FORM_QUALIF = u"Qualifiante"
    FORM_CERTI = u"Certifiante"
    FORM_STAGE = u"Stage"
    FORM_CHOIX = ((FORM_QUALIF, FORM_QUALIF),
                  (FORM_CERTI, FORM_CERTI),
                  (FORM_STAGE, FORM_STAGE))
    form_formation1 = models.TextField(u"Formation 1 (et organisme)", null=True, blank=True)
    form_type1 = models.CharField("Type de formation", max_length=15, choices=FORM_CHOIX, null=True, blank=True)
    form_formation2 = models.TextField(u"Formation 2 (et organisme)", null=True, blank=True)
    form_type2 = models.CharField("Type de formation", max_length=15, choices=FORM_CHOIX, null=True, blank=True)
    
    #Autres compétences
    autrComp_ling = models.TextField(u"Linguisitiques", null=True, blank=True)
    autrComp_info = models.TextField(u"Informatiques", null=True, blank=True)
    autrComp_autr = models.TextField(u"Autres", null=True, blank=True)
    
    