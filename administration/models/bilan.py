# -*- coding: utf-8 -*-
from django.db import models
from greta.administration.models import LettreCommande


class Bilan(models.Model):
    
    
    class Meta:
        app_label = 'administration' 
        verbose_name = u"Bilan"
        verbose_name_plural = u"Bilan"

    lettre_commande = models.OneToOneField('LettreCommande')
    inscritAle = models.DateField(null=True, blank=True)
    
    # Correspondant ALE
    aleCor_nom = models.CharField(u"Nom et prénom", max_length=100, null=True, blank=True)
    aleCor_tel = models.CharField(u"Téléphone", max_length=100, null=True, blank=True)
    aleCor_mail = models.EmailField(u"Mail", max_length=100, null=True, blank=True)
    
    # Situation en fin d'accompagnement - emploi
    emploi_posteOcc = models.TextField(u"Poste occupé", null=True, blank=True)
    emploi_codeRome = models.CharField(u"Code ROME", max_length=20, null=True, blank=True)
    CDI = u"CDI"
    CDD = u"CDD"
    CA = u"Contrat aidé"
    AU = u"Autre"
    CONTRAT = ((CDI, CDI),
               (CDD, CDD),
               (CA, CA),
               (AU, AU))
    emploi_typeContrat = models.CharField(u"Type de contrat", max_length=20, choices=CONTRAT, null=True, blank=True)
    emploi_CADetails = models.TextField(u"Si contrat aidé, précisez le type de contrat", null=True, blank=True)
    emploi_AUDetails = models.TextField(u"Si autre, précisez", null=True, blank=True)
    emploi_debut = models.DateField(null=True, blank=True)
    emploi_fin = models.DateField(null=True, blank=True)
    emploi_duree = models.CharField(u"Durée hebdomadaire", max_length=100, null=True, blank=True)
    emploi_coord = models.TextField(u"Nom et adresse de l'entreprise", null=True, blank=True)
    
    # Situation en fin d'accompagnement - formation
    form_intitule = models.CharField(u"Intitulé", max_length=200, null=True, blank=True)
    form_coor = models.TextField(u"Nom et coordonnées de l'organisme", null=True, blank=True)
    form_objectif = models.TextField(u"Objectif", null=True, blank=True)
    form_heure = models.IntegerField(u"Nombre d'heures", null=True, blank=True)
    form_debut = models.DateField(null=True, blank=True)
    form_fin = models.DateField(null=True, blank=True)
    
    # Situation en fin d'accompagnement - création d'entreprise
    entr_nature = models.TextField(u"Nature du projet", null=True, blank=True)
    entr_lieu = models.CharField(u"Lieu", max_length=100, null=True, blank=True)
    entr_date = models.DateField(null=True, blank=True)
    ENTRE_ONE = u"Demande de doosier d'ACCRE"
    ENTRE_TWO = u"Attestation de dépôt de demande d'immatriculation auprès d'un centre de formalité des entreprises"
    ENTRE_THREE = u"Attestation de dépôt de dossier de ...."
    ENTRE_FOUR = u"Demande d'immatriculation au registre du commerce"
    ENTRE_FIVE = u"Autres documents à préciser...."
    ENTR_JUSTI = ((ENTRE_ONE, ENTRE_ONE),
                  (ENTRE_TWO, ENTRE_TWO),
                  (ENTRE_THREE, ENTRE_THREE),
                  (ENTRE_FOUR, ENTRE_FOUR),
                  (ENTRE_FIVE, ENTRE_FIVE)
                  )
    entr_justifcatif = models.CharField(u"Type de contrat", max_length=200, choices=ENTR_JUSTI, null=True, blank=True)
    entr_dossier = models.TextField(u"Si dépôt de dossier, précisez", null=True, blank=True)
    entr_docs = models.TextField(u"Si autres documents, précisez", null=True, blank=True)
    
    # Situation en fin d'accompagnement - toujours à la recherche d'un emploi
    rech_intit = models.TextField(u"Intitulés des emplois/métiers recherchés", null=True, blank=True)
    rech_rome = models.TextField(u"Code ROME des emplois/métiers recherchés", null=True, blank=True)
    rech_sect = models.TextField(u"Secteur d'activité des emplois/métiers recherchés", null=True, blank=True)
    rech_zone = models.TextField(u"Zones géographiques des emplois/métiers recherchés", null=True, blank=True)
    
    # Situation en fin d'accompagnement - cessation d'incription
    cess_date = models.DateField(null=True, blank=True)
    cess_moti = models.TextField(u"Préciser le motif", null=True, blank=True)
    
    # Actions réalisées pendant l'accompagnement - Stabilisation du ou dzes métiers recherchés/ Elaboration du 
    # projet professionnel (à détailler par rapport aux fichiers ROME des emploi concernés)
    action_comp = models.TextField(u"Compétences acquises et transférables", null=True, blank=True)
    action_cogn = models.TextField(u"Capacités cognitives", null=True, blank=True)
    action_rela = models.TextField(u"Capacités relationnelles", null=True, blank=True)
    action_P1_deb = models.DateField(null=True, blank=True)
    action_P1_fin = models.DateField(null=True, blank=True)
    action_P1_coord = models.TextField(u"Période en entreprise 1 - Nom et adresse de l'entreprise", null=True, blank=True)
    action_P1_res = models.TextField(u"Période en entreprise 1 - Résultats (pistes dégagées)", null=True, blank=True)
    action_P1_comp = models.TextField(u"Période en entreprise 1 - Compétences à acquérir", null=True, blank=True)
    action_P2_deb = models.DateField(null=True, blank=True)
    action_P2_fin = models.DateField(null=True, blank=True)
    action_P2_coord = models.TextField(u"Période en entreprise 2 - Nom et adresse de l'entreprise", null=True, blank=True)
    action_P2_res = models.TextField(u"Période en entreprise 2 - Résultats (pistes dégagées)", null=True, blank=True)
    action_P2_comp = models.TextField(u"Période en entreprise 2 - Compétences à acquérir", null=True, blank=True)
    
    # Actions réalisées pendant l'accompagnement -
    # Accompagnement vers l'emploi/pistes d'emploi
    action_nbOE = models.PositiveIntegerField(u"Nombre d'OE corresondant à l'emploi recherché", null=True, blank=True)
    action_nbCa = models.PositiveIntegerField(u"Nombre de candidatures sur ces offres", null=True, blank=True)
    action_nbEN = models.PositiveIntegerField(u"Nombre d'entretiens d'embauches obtenus", null=True, blank=True)
    action_autreEmp = models.TextField(u"Autres emplois recherchés (nom des emplois (codes ROME -----   -----  -----)", null=True, blank=True)
    action_autreSect = models.TextField(u"Autres secteurs professionnels", null=True, blank=True)
    action_autreAct = models.TextField(u"Autres activités", null=True, blank=True)
    action_sect = models.TextField(u"Secteurs géographiques", null=True, blank=True)
    
    # Actions réalisées pendant l'accompagnement -
    # Suivi dans l'emploi
    action_reprCont = models.TextField(u"Contexte général de votre reprise d'emploi", null=True, blank=True)
    action_reprDiff = models.TextField(u"Difficultés rencontrées", null=True, blank=True)
    action_reprRep = models.TextField(u"Réponses apportées", null=True, blank=True)
    action_reprEntr = models.PositiveIntegerField(u"Nombre d'entretiens de suivis", null=True, blank=True)
    action_reprMod= models.TextField(u"Modalités (déplacement demandeur d'emploi/référent/téléphone)", null=True, blank=True)
    
    
    # Actions priorotaires à mener à l'issue de la prestation 
    # (pour les personnes n'ayant pas trouvé de solutions (emploi/formation/créations d'entreprises))
    actionPrio_A1_date = models.CharField(u"Action 1 - Date", max_length=200, null=True, blank=True)
    actionPrio_A1_action = models.TextField(u"Action 1 - Action", null=True, blank=True)
    actionPrio_A1_demarche = models.TextField(u"Action 1 - Démarches à effectuer", null=True, blank=True)
    
    actionPrio_A2_date = models.CharField(u"Action 2 - Date", max_length=200, null=True, blank=True)
    actionPrio_A2_action = models.TextField(u"Action 2 - Action", null=True, blank=True)
    actionPrio_A2_demarche = models.TextField(u"Action 2 - Démarches à effectuer", null=True, blank=True)
    
    actionPrio_A3_date = models.CharField(u"Action 3 - Date", max_length=200, null=True, blank=True)
    actionPrio_A3_action = models.TextField(u"Action 3 - Action", null=True, blank=True)
    actionPrio_A3_demarche = models.TextField(u"Action 3 - Démarches à effectuer", null=True, blank=True)
    
    # Conclusion
    conc_obsref = models.TextField(u"Observations du référent", null=True, blank=True)
    conc_obsbene = models.TextField(u"Observations du bénéficiaire", null=True, blank=True)
    conc_datesuivi = models.CharField(u"Date de suivi à 3 mois", max_length=200, null=True, blank=True)
    conc_cons = models.TextField(u"Conseiller prescripteur (nom, prénom, ALE)", null=True, blank=True)
    conc_datenext = models.DateField(null=True, blank=True)
    conc_date = models.DateField(null=True, blank=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     

    
    
    