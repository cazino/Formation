# -*- coding: utf-8 -*-
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib import colors, enums, styles
from reportlab.graphics.shapes import Drawing, Rect
from greta.administration.models import LettreCommande, ouvertureRdv
import common

class evenementBase(object):
    
    # ZONE
    EST = u"93-94"
    SUD_EST = u"77-91"
    
    # TYPE
    DEBUT = "DEBUT"
    ABANDON = "ABANDON"
    
    
    elements = []
    petitePolice = 10
    basePolice  = 12
    grandePolice = 14
    fontsize_style = ('FONTSIZE',(0,0),(-1,-1),basePolice)
    
    paragraph_style = styles.getSampleStyleSheet()['Normal']
    paragraph_style.fontSize = basePolice
    paragraph_style.spaceAfter = 10
    paragraph_style.alignment = enums.TA_LEFT
    
    
    
    
    empty_checkbox = Image(common.rootPath+"checkbox_empty.jpg", width=18, height=18)
    checked_checkbox = Image(common.rootPath+"checkbox_checked.jpg", width=18, height=18)
    
    
    
    def __init__(self, response, lettre_commande):
        super(evenementBase, self).__init__()
        self.response = response
        self.lettre_commande = lettre_commande
        self.doc = SimpleDocTemplate(self.response, rightMargin=10, leftMargin=10, topMargin=0, bottomMargin=5)
    
    def __get_image_ouverture_rdv(self, ouverture_rdv, related_statut, typeEvennement):
        if (ouverture_rdv.statut == related_statut and typeEvennement == self.DEBUT):
            return self.checked_checkbox
        return self.empty_checkbox

    def __get_comments_ouverture_rdv(self, ouverture_rdv, typeEvennement):
        if ouverture_rdv.statut == ouvertureRdv.PRESENT_NC and typeEvennement == self.DEBUT:
            return  ouverture_rdv.motif
        return ""
    
    def __get_newdateheure_ouverture_rdv(self, ouverture_rdv, typeEvennement):
        if ouverture_rdv.statut == ouvertureRdv.REPORT and typeEvennement == self.DEBUT:
            return  ouverture_rdv.dateheure_nouveauRdv
        return None

    def __get_newdate_ouverture_rdv(self, ouverture_rdv, typeEvennement):
        newdateheure = self.__get_newdateheure_ouverture_rdv(ouverture_rdv, typeEvennement)
        if newdateheure:
            return  newdateheure.date().strftime(common.date_format)
        return ''

    def __get_newtime_ouverture_rdv(self, ouverture_rdv, typeEvennement):
        newdateheure = self.__get_newdateheure_ouverture_rdv(ouverture_rdv, typeEvennement)
        if newdateheure:
            return  newdateheure.time().strftime("%H:%M")
        return ''
    
    def __typepresta_checkbox(self):
        result = []
        for a, b in LettreCommande.TYPES_PRESTA:
            if a != LettreCommande.AUTRE:
                if a==self.lettre_commande.type_presta:
                    result.append(self.checked_checkbox)
                else:
                    result.append(self.empty_checkbox)
                result.append(a)
        return result
                
        
    def __autreTypePresta_checkbox(self):
        if LettreCommande.AUTRE == self.lettre_commande.type_presta:
            return self.checked_checkbox
        return self.empty_checkbox
    
    def __prestaType_precisions(self):
        if LettreCommande.AUTRE == self.lettre_commande.type_presta:
            return self.lettre_commande.typePresta_autre
        return ''
    
    
    def __headImage(self, zone):
        if zone == self.EST:
            imagePath = common.rootPath+"evenement_est.jpg"
        else: #zone == self.SUD-EST
            imagePath = common.rootPath+"evenement_sud_est.jpg"
        evenement_Image = Image(imagePath, width=484 , height=102)
        evenement_Image.spaceAfter = 30
        self.elements.append(evenement_Image)
    
    def __type_prestation_firstrow(self):
        self.elements.append(Paragraph("<u>Type de prestation</u>", styles.getSampleStyleSheet()['Heading2']))
        typePresta_data = [self.__typepresta_checkbox()]
        colonnesWidths =    (20, 40, 20, 45, 20, 60, 20, 45, 20, 45, 20, 40, 20, 40, 20, 35, 20, 45)
        #colonnesWidths =    (20, 40, 20, 45, 20, 60, 20, 45, 20, 45, 20, 40, 20, 40)                                                          
        typePresta_style = TableStyle([self.fontsize_style,
                                       ('VALIGN',(1,0),(1,0),'MIDDLE'),
                                       ('VALIGN',(3,0),(3,0),'MIDDLE'),
                                       ('VALIGN',(5,0),(5,0),'MIDDLE'),
                                       ('VALIGN',(7,0),(7,0),'MIDDLE'),
                                       ('VALIGN',(9,0),(9,0),'MIDDLE'),
                                       ('VALIGN',(11,0),(11,0),'MIDDLE'),
                                       ('VALIGN',(13,0),(13,0),'MIDDLE'),
                                       ('VALIGN',(13,0),(13,0),'MIDDLE'),
                                       ('VALIGN',(15,0),(15,0),'MIDDLE'),
                                       ('VALIGN',(17,0),(17,0),'MIDDLE'),
                                       ])
        typePresta_style.spaceAfter = 10
        typePresta_table = Table(data=typePresta_data, colWidths=colonnesWidths, style=typePresta_style)
        self.elements.append(typePresta_table)
        
    def __type_prestation_secondrow(self):
        typePresta_data = [[ self.__autreTypePresta_checkbox(), Paragraph(u"Autre prestatation (à préciser):"+self.__prestaType_precisions(), self.paragraph_style)],]
        typePresta_style = TableStyle([self.fontsize_style,('VALIGN',(1,0),(1,0),'MIDDLE')])
        colWidths=[25, 500]
        typePresta_table = Table(data=typePresta_data, style=typePresta_style, colWidths=colWidths)
        typePresta_table.spaceAfter = 20
        typePresta_table.hAlign = 0
        self.elements.append(typePresta_table)
        
    def __type_presta(self):
        self.__type_prestation_firstrow()
        self.__type_prestation_secondrow()
    
    def __lc_details(self):        
        self.elements.append(Paragraph(u"<font size='12'><b>N° Lettre de Commande: </b>%s</font>" % (self.lettre_commande.numero_lc,), self.paragraph_style))
        self.elements.append(Paragraph(u"<font size='12'><b>Nom du prestataire: </b>%s</font>" % (self.lettre_commande.site.prestataire.nom,), self.paragraph_style))
        self.elements.append(Paragraph(u"<font size='12'><b>Lieu de réalisation: </b>%s</font>" % (self.lettre_commande.site.ville,), self.paragraph_style))
        self.elements.append(Paragraph(u"<font size='12'><b>Agence d'inscription: </b>%s</font>" % (self.lettre_commande.ale_prescriptrice,), self.paragraph_style))
        self.elements.append(Paragraph(u"<font size='12'><b>Nom Prénom du DE: </b>%s</font>" % (self.lettre_commande.nom+" "+self.lettre_commande.prenom,), self.paragraph_style))
        self.elements.append(Paragraph(u"<font size='12'><b>N°Identifiant: </b>%s</font>" % (self.lettre_commande.polemploi_id,), self.paragraph_style))
        self.elements.append(Paragraph(u"<font size='12'><b>Date et heure du premier Rendez-vous: </b>%s</font>" % (self.lettre_commande.ouverture_rdv.dateheure.strftime("%d/%m/%Y %H:%M"),), self.paragraph_style))
    
    def __barre_horizontale(self):
        barreHorizontale = Image(common.rootPath+"barre_horizontale.jpg", width=520, height=6)
        barreHorizontale.spaceAfter = 20
        self.elements.append(barreHorizontale)
        
    def __ouvertureBaseSpace(self, table):
        table.hAlign = 0
        table.spaceAfter = 10
        
    def __ouvertureBase(self, typeEvenement, choixDebutPresta, legendeChoixDebutPresta):
        #__get_image_ouverture_rdv(ouverture_rdv, related_statut, typeEvennement)
        demarragePresta_data = [[self.__get_image_ouverture_rdv(self.lettre_commande.ouverture_rdv, choixDebutPresta, typeEvenement), legendeChoixDebutPresta],]
        demarragePresta_style = TableStyle([('FONTSIZE', (1,0), (1,0), self.grandePolice),
                                            ('LEADING', (1,0), (1,0), 3),
                                            ('VALIGN',(1,0),(1,0),'TOP'),])
        demarragePresta = Table(demarragePresta_data, style=demarragePresta_style)
        self.__ouvertureBaseSpace(demarragePresta)
        self.elements.append(demarragePresta)

    def __refusPrestaMotif(self, typeEvenement):
        refusPresta_data = [[None,  Paragraph(u"<strong>Indiquer le motif: </strong>" + self.__get_comments_ouverture_rdv(self.lettre_commande.ouverture_rdv, typeEvenement), self.paragraph_style)],]
        refusPresta_style = TableStyle([('FONTSIZE', (0, 0), (-1, -1), self.grandePolice),])
        colWidths = [25, 500]
        refusPresta = Table(refusPresta_data, style=refusPresta_style, colWidths=colWidths)
        self.__ouvertureBaseSpace(refusPresta) 
        self.elements.append(refusPresta)
        
    def __nouveauRdv(self, typeEvenement):
        newDateTime_data = [[None, "Date du nouveau RDV: "+self.__get_newdate_ouverture_rdv(self.lettre_commande.ouverture_rdv, typeEvenement), "Heure du nouveau RDV: "+self.__get_newtime_ouverture_rdv(self.lettre_commande.ouverture_rdv, typeEvenement)],]
        newDateTime_style = TableStyle([('FONTSIZE', (0,0), (-1,-1), self.basePolice), ])
        newDateTime = Table(newDateTime_data, style=newDateTime_style)
        self.__ouvertureBaseSpace(newDateTime)
        self.elements.append(newDateTime)
        
    def __lc_ouverture(self, typeEvenement):
        self.__ouvertureBase(typeEvenement, ouvertureRdv.PRESENT_C, u"A DEMARRE LA PRESTATION")
        self.__ouvertureBase(typeEvenement, ouvertureRdv.PRESENT_NC, u"N'A PAS ADHERE A LA PRESTATION")
        self.__refusPrestaMotif(typeEvenement)
        self.__ouvertureBase(typeEvenement, ouvertureRdv.ABSENT, u"NE S'EST PAS PRESENTE")
        self.__ouvertureBase(typeEvenement, ouvertureRdv.REPORT, u"A DEMANDE AU PRESTATAIRE UN REPORT DU PREMIER RDV (8 jours maxi)")
        self.__nouveauRdv(typeEvenement)
        
    def __abandon_checkbox(self, typeEvenement):
        if typeEvenement == self.ABANDON:
            return self.checked_checkbox
        return self.empty_checkbox  
    
    def __abandon_date(self, typeEvenement):
        if typeEvenement == self.ABANDON:
            return self.lettre_commande.cloture.date_abandon.strftime(common.date_format)
        return ''  
    
    def __abandon_motif(self, typeEvenement):
        if typeEvenement == self.ABANDON:
            return self.lettre_commande.cloture.motif.replace('\r', '')
        return ''  
    
    def __lc_abandon(self, typeEvenement):
        abandonPresta_data = [[self.__abandon_checkbox(typeEvenement), u"A ABANDONNE EN COURS DE PRESTATION A LA DATE DU: " + self.__abandon_date(typeEvenement)],
                              [None, Paragraph(u"<strong>Indiquer le motif: </strong>" + self.__abandon_motif(typeEvenement), self.paragraph_style) ]
                          ]
        colWidths = [25, 500]
        abandonPresta_style = TableStyle([('FONTSIZE', (1,0), (1,0), self.grandePolice),
                                      ('VALIGN',(1,0),(1,0),'TOP'),
                                      ('FONTSIZE', (1,1), (1,1), self.basePolice),
                                      ])
        abandonPresta = Table(abandonPresta_data, style=abandonPresta_style, colWidths=colWidths)
        abandonPresta.hAlign = 0
        abandonPresta.spaceAfter = 20
        self.elements.append(abandonPresta)
    
        
    def __pidedepage(self):
        pdp_style = styles.getSampleStyleSheet()['Normal']
        pdp_style.alignment = enums.TA_CENTER
        p1 = Paragraph(u"<font size='12'>LES EVENEMENTS DOIVENT ETRE SIGNALES A LA PLATEFORME-DES QUE POSSIBLE ET AU PLUS TARD DANS LES 48 HEURES</font>", pdp_style)
        p2 = Paragraph(u"<font size='12'>01 49 44 42 86</font>", pdp_style)
        pdp_data = [[p1,],
                    [p2,]] 
        pdp_style = TableStyle([('FONTSIZE', (0,0), (-1,-1), self.grandePolice),])
        self.elements.append(Table(data=pdp_data, style=pdp_style, colWidths=[500,]))
        
        
    def buildDoc(self, typeEvenement, zone):
        self.__headImage(zone)
        self.__type_presta()
        self.__lc_details()
        self.__barre_horizontale()
        self.__lc_ouverture(typeEvenement)
        self.__barre_horizontale()
        self.__lc_abandon(typeEvenement)
        self.__barre_horizontale()
        self.__pidedepage()
        self.doc.build(self.elements)
        
        
        
        
