# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from greta.administration.models import Bilan
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import ParagraphStyle, PropertySet
from reportlab.lib.colors import black, darkred
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from gretaview import GretaView  
import common
from utils import change_lines


class rdvView(GretaView):
    
    def __init__(self, rdv):
        self.rdv = rdv
    
    def _persoEvenDate(self, number):
        return self._optionalField('self.rdv.accsoc_date'+str(number))
    
    def _persoEvenInsti(self, number):
        return self._optionalField('self.rdv.accsoc_insti'+str(number))
    
    def _persoEvenAction(self, number):
        return self._optionalField('self.rdv.accsoc_action'+str(number))
    
    def _persoEvenResults(self, number):
        return self._optionalField('self.rdv.accsoc_results'+str(number))
        
    def _persoEven(self, number): 
        champs = [self._persoEvenDate(number), self._persoEvenInsti(number), self._persoEvenAction(number), self._persoEvenResults(number)]
        if champs == ['', '', '', '']:
            return []
        else:
            return champs
       
    def persoAllEvents(self):
        result = []
        for evenNumber in range(1, 5):
            tmpList = self._persoEven(evenNumber)
            if tmpList != []:
                result.append(tmpList)
        return result
    
    
    def _emploiEvenDate(self, number):
        return self._optionalField('self.rdv.accemp_date'+str(number))
    
    def _emploiEvenEntr(self, number):
        return self._optionalField('self.rdv.accemp_entr'+str(number))
    
    def _emploiEvenMod(self, number):
        return self._optionalField('self.rdv.accemp_mod'+str(number))
    
    def _emploiEvenResults(self, number):
        return self._optionalField('self.rdv.accemp_results'+str(number))
        
    def _emploiEven(self, number): 
        champs = [self._emploiEvenDate(number), self._emploiEvenEntr(number), self._emploiEvenMod(number), self._emploiEvenResults(number)]
        if champs == ['', '', '', '']:
            return []
        else:
            return champs
    
    def emploiAllEvents(self):
        result = []
        for evenNumber in range(1, 5):
            tmpList = self._emploiEven(evenNumber)
            if tmpList != []:
                result.append(tmpList)
        return result
        

class bilanView(GretaView):
    
    def __init__(self, lc):
        self.lc = lc

        
    def datedebut(self):
        return self.lc.date_debut.strftime(common.date_format)
    
    def datefin(self):
        return self.lc.dernier_jour_presta()
    
    def num(self):
        return self._optionalField('self.lc.numero_lc')
    
    def nomprenom(self):
        return self.lc.nom+" "+self.lc.prenom
    
    def CInomprenom(self):
        return self.lc.charge_insertion.nom+" "+self.lc.charge_insertion.prenom
     
    def ALEnomprenom(self):
        return self._optionalField('self.lc.bilan.aleCor_nom')
           
    def idALE(self):
        return self.lc.polemploi_id
    
    def LCtel(self):
        return self._optionalField('self.lc.etat_civil.telfixe')
        
    def LCmail(self):
        return self._optionalField('self.lc.etat_civil.mail')
        
    def organismeReferent(self):
        return self.lc.site.prestataire.nom
    
    def ALEnom(self):
        return self.lc.ale_prescriptrice
    
    def incritALE(self):
        return self._optionalField('self.lc.ale_prescriptrice')
         
    def refTel(self):
        return self._optionalField('self.lc.charge_insertion.tel_fixe')
        
    def refMail(self):
        return self._optionalField('self.lc.charge_insertion.mail')
        
    def ALEtel(self):
        return self._optionalField('self.lc.bilan.aleCor_tel')
        
    def ALEmail(self):
        return self._optionalField('self.lc.bilan.aleCor_mail')
        
    # Situation en fin d'accompagnenement
    
    def postOcc(self):
        return self._optionalField('self.lc.bilan.emploi_posteOcc')
    
    def rom(self):        
        return self._optionalField('self.lc.bilan.emploi_codeRome')
    
    def typecontrat(self):
        contrat_type = self._optionalField('self.lc.bilan.emploi_typeContrat')
        precision = ''
        if contrat_type==Bilan.CA:
            precision = self._optionalField('self.lc.bilan.emploi_CADetails')
        if contrat_type==Bilan.AU:
            precision = self._optionalField('self.lc.bilan.emploi_AUDetails')
        return contrat_type+" - "+precision
     
    def empldeb(self):
        return self._optionalDateField('self.lc.bilan.emploi_debut')
    
    def emplfin(self):
        return self._optionalDateField('self.lc.bilan.emploi_fin') 
    
    def dureehebd(self):
         return self._optionalField('self.lc.bilan.emploi_duree') 
     
    def emplcoord(self):
        return self._optionalField('self.lc.bilan.emploi_coord')
    
    def formint(self):
        return self._optionalField('self.lc.bilan.form_intitule')
    
    def formcoor(self):
        return self._optionalField('self.lc.bilan.form_coor')
    
    def formobj(self):
        return self._optionalField('self.lc.bilan.form_objectif')
    
    def formheures(self):
        return str(self._optionalField('self.lc.bilan.form_heure'))
    
    def formentre(self):
        return self._optionalDateField('self.lc.bilan.form_debut')
        
    def formsortie(self):    
        return self._optionalDateField('self.lc.bilan.form_fin')
    
    def entrproj(self):
        return self._optionalField('self.lc.bilan.entr_nature')
    
    def entrlieu(self):
        return self._optionalField('self.lc.bilan.entr_lieu')
    
    def entrdate(self):
        return self._optionalDateField('self.lc.bilan.entr_date')
    
    def entrjusti(self):
        res1 = self._optionalField('self.lc.bilan.entr_justifcatif')
        res2 = ''
        if res1==Bilan.ENTRE_THREE:
            res2 = self._optionalField('self.lc.bilan.entr_dossier')
        if res1==Bilan.ENTRE_FIVE:
            res2 = self._optionalField('self.lc.bilan.entr_docs')
        return res1+u" - "+res2
    
    def rech_int(self):
        return self._optionalField('self.lc.bilan.rech_intit')
        
    def rech_rome(self):
        return self._optionalField('self.lc.bilan.rech_rome')
    
    def rech_act(self):
        return self._optionalField('self.lc.bilan.rech_sect')
    
    def rech_zones(self):
        return self._optionalField('self.lc.bilan.rech_zone')
    
    def cess_date(self):
        return self._optionalDateField('self.lc.bilan.cess_date')
    
    def cess_motif(self):
        return self._optionalField('self.lc.bilan.cess_moti')
    
    # Actions réalisées pendant votre accompagnement
    def persoAllEvents(self):
        result = []
        lesRdv = self.lc.rdv.all().order_by('dateheure')
        for rdv in lesRdv:
            result += rdvView(rdv).persoAllEvents()
        return result
        
    def action_comp(self):
        return self._optionalField('self.lc.bilan.action_comp')
    
    def action_cogn(self):
        return self._optionalField('self.lc.bilan.action_cogn')
    
    def action_rela(self):
        return self._optionalField('self.lc.bilan.action_rela')
    
    
    def action_P_deb(self, number):
        return self._optionalDateField('self.lc.bilan.action_P'+str(number)+'_deb')
    
    def action_P_fin(self, number):
        return self._optionalDateField('self.lc.bilan.action_P'+str(number)+'_fin')
    
    def action_P_coord(self, number):
        return self._optionalField('self.lc.bilan.action_P'+str(number)+'_coord')
    
    def action_P_res(self, number):
        return self._optionalField('self.lc.bilan.action_P'+str(number)+'_res')
    
    def action_P_comp(self, number):
        return self._optionalField('self.lc.bilan.action_P'+str(number)+'_comp')
    
    def action_nbOE(self):
        return str(self._optionalField('self.lc.bilan.action_nbOE'))
        
    def action_nbCa(self):
        return str(self._optionalField('self.lc.bilan.action_nbCa'))
    
    def action_nbEN(self):
        return str(self._optionalField('self.lc.bilan.action_nbEN'))
    
    def action_autreEmp(self):
        return self._optionalField('self.lc.bilan.action_autreEmp')
    
    def action_autreSect(self):
        return self._optionalField('self.lc.bilan.action_autreSect')
    
    def action_autreAct(self):
        return self._optionalField('self.lc.bilan.action_autreAct')
    
    def action_sect(self):
        return self._optionalField('self.lc.bilan.action_sect')
         
    def emploiAllEvents(self):
        result = []
        lesRdv = self.lc.rdv.all().order_by('dateheure')
        for rdv in lesRdv:
            result += rdvView(rdv).emploiAllEvents()
        return result
    
    def action_reprCont(self):
        return self._optionalField('self.lc.bilan.action_reprCont')
    
    def action_reprDiff(self):
        return self._optionalField('self.lc.bilan.action_reprDiff')
    
    def action_reprRep(self):
        return self._optionalField('self.lc.bilan.action_reprRep')
    
    def action_reprEntr(self):
        return str(self._optionalField('self.lc.bilan.action_reprEntr'))
    
    def action_reprMod(self):
        return self._optionalField('self.lc.bilan.action_reprMod')
    
    def lesactionsPrio(self):
        result = []
        for i in range(1, 4):
            tmpList = [self._optionalField('self.lc.bilan.actionPrio_A'+str(i)+'_date'),
                       self._optionalField('self.lc.bilan.actionPrio_A'+str(i)+'_action'),
                       self._optionalField('self.lc.bilan.actionPrio_A'+str(i)+'_demarche'),
                       ]
            if tmpList != ['', '', '']:
                result.append(tmpList)
        return result
                
    def conc_obsref(self):
        return self._optionalField('self.lc.bilan.conc_obsref')            
    
    def conc_obsbene(self):
        return self._optionalField('self.lc.bilan.conc_obsbene')
    
    def conc_datesuivi(self):
        return self._optionalField('self.lc.bilan.conc_datesuivi')
    
    def conc_cons(self):
        return self._optionalField('self.lc.bilan.conc_cons')
    
    def conc_datenext(self):
        return self._optionalDateField('self.lc.bilan.conc_datenext')
    
    def conc_date(self):
        return self._optionalDateField('self.lc.bilan.conc_date')
 
 
    
class styleGetter(object):
        
    def getstyle(self, style):
        if style=='style1':
            return ParagraphStyle(name='style1', fontName='Times-Roman', fontSize=16, textColor=darkred) 
        if style=='style2':
            return ParagraphStyle(name='style2', fontName='Times-Roman', fontSize=12, textColor=darkred)        
        if style=='style3':
            return ParagraphStyle(name='style3', fontName='Times-Roman', fontSize=11, textColor=darkred)
        if style=='style4':
            return ParagraphStyle(name='style4', fontName='Times-Roman', fontSize=9, textColor=darkred)        
        if style=='style5':
            return ParagraphStyle(name='style5', fontName='Times-Roman', fontSize=8, textColor=darkred)
        if style=='bullet-style3':
            return ParagraphStyle(name='bullet-style3', 
                                  fontName='Times-Roman',
                                  fontSize=11, 
                                  textColor=darkred,
                                  bulletIndent=20, 
                                  bulletFontName='Symbol',
                                  )
        if style=='style_base':
            return ParagraphStyle(name='style_base', fontName='Times-Roman', fontSize=11, textColor=black)
    getstyle = classmethod(getstyle)
    
    def getPara(self, style, text, spaceAfter=0):    
        style_para = styleGetter.getstyle(style)
        style_para.spaceAfter = spaceAfter
        return Paragraph(text, style=style_para)
    getPara = classmethod(getPara)
        
    def getBulletPara(self, text):
        style_para = styleGetter.getstyle('bullet-style3')
        style_para.spaceAfter = 5
        return Paragraph(u"<b>"+text+"</b>", style=style_para, bulletText='-')
    getBulletPara = classmethod(getBulletPara)
    
    def getTableauStyle(self):
        return TableStyle([('GRID', (0,0), (-1,-1), 0.25, black),
                           ('VALIGN',(0,0),(-1,-1),'TOP'),
                          ])
    getTableauStyle = classmethod(getTableauStyle)   
        
    def getTableau(self, data, spaceAfter=0):
        style = styleGetter.getTableauStyle()
        style.spaceAfter = spaceAfter
        return Table(data=data, style=style)     
    getTableau = classmethod(getTableau)
    
    
class MyStyleSheet(object):
    
    def get(self, style_name, **kw):
        if style_name == 'style1':
            return ParagraphStyle(name='style1', fontName='Times-Roman', fontSize=16, textColor=darkred, **kw) 
        if style_name == 'style2':
            return ParagraphStyle(name='style2', fontName='Times-Roman', fontSize=12, textColor=darkred, **kw)        
        if style_name == 'style3':
            return ParagraphStyle(name='style3', fontName='Times-Roman', fontSize=11, textColor=darkred, **kw)
        if style_name == 'style4':
            return ParagraphStyle(name='style4', fontName='Times-Roman', fontSize=9, textColor=darkred, **kw)        
        if style_name == 'style5':
            return ParagraphStyle(name='style5', fontName='Times-Roman', fontSize=8, textColor=darkred, **kw)
        if style_name == 'bullet-style3':
            return ParagraphStyle(name='bullet-style3', 
                                  fontName='Times-Roman',
                                  fontSize=11, 
                                  textColor=darkred,
                                  bulletIndent=20, 
                                  bulletFontName='Symbol',
                                  **kw
                                  )
        if style_name == 'style_base':
            return ParagraphStyle(name='style_base', fontName='Times-Roman', fontSize=11, textColor=black, **kw)
    get = classmethod(get)    


class MyParagraph(Paragraph):
    
    def __init__(self, text, style, bulletText=None, **kw):
        Paragraph.__init__(self, text.replace('&', 'et'), bulletText=bulletText, style=MyStyleSheet.get(style, **kw))
        
        
    
class bilanDoc(object):
        
    def __init__(self, response, lc):
        self.bilanView = bilanView(lc) 
        self.doctemplate = SimpleDocTemplate(response, rightMargin=20, leftMargin=20, topMargin=10, bottomMargin=10)
        self.story = []
        
    def append(self, text, style, bulletText=None, **kw):
        for line in change_lines(text).split("\n"):
            #if line != "\n" and line != "\r":
            self.story.append(MyParagraph(text=line, style=style, bulletText=bulletText, **kw))
        
    def entete(self):
        image = Image(common.rootPath+'pole_emploi.jpg', width=128, height=82)
        image.hAlign = 'LEFT'
        para = MyParagraph(style='style3', text=u"<i>Avec le soutien du Fonds Social Européen</i>", alignment=TA_RIGHT, spaceAfter=20)
        self.story.append(image)
        self.story.append(para)
        
    def head(self):
        para1 = MyParagraph("<b>Mobilisation vers l'emploi</b>", 'style1', spaceAfter=15, alignment=TA_CENTER)
        para2 = MyParagraph("<b><i>Bilan à l'issue de la prestation</i><b>", 'style2', spaceAfter=20, alignment=TA_CENTER)
        self.story.append(para1)
        self.story.append(para2)
        
    def intro(self):
        self.story.append(MyParagraph(u"<b>Accompagnement personnalisé du <font color=black>"+self.bilanView.datedebut()+u"</font> au <font color=black>"+self.bilanView.datefin()+u"</font> Commande n° <font color=black>"+self.bilanView.num()+u"</font></b>", 'style3', spaceAfter=5))
        
    def tableau_intro(self):
        style_tableau = TableStyle([('BOX', (0,0), (0,-1), 0.25, black),
                                    ('BOX', (1,0), (1,-1), 0.25, black),
                                    ('BOX', (2,0), (2,-1), 0.25, black),
                                    ('BOX', (0,0), (-1,0), 0.25, black),
                                    ('VALIGN',(0,0),(-1,-1),'TOP'),
                                    ])
        style_tableau.spaceAfter = 10
        tableau_data = [[MyParagraph(style='style3', text=u"<b>Bénéficiaire</b>"), MyParagraph(style='style3', text=u"<b>Référent</b>"), MyParagraph(style='style3', text=u"<b>Correspondant ALE</b>")],    
                        [MyParagraph(style='style3', text=u"<b>Nom Prénom : <font color=black>"+self.bilanView.nomprenom()+"</font></b>"), MyParagraph(style='style3', text=u"<b>Nom Prénom : <font color=black>"+self.bilanView.CInomprenom()+"</font></b>"), MyParagraph(style='style3', text=u"<b>Nom Prénom : <font color=black>"+self.bilanView.ALEnomprenom()+"</font></b>")],
                        [MyParagraph(style='style3', text=u"<b>Identifiant n° : <font color=black>"+self.bilanView.idALE()+"</font></b>"), MyParagraph(style='style3', text=u"<b>Organisme : <font color=black>"+self.bilanView.organismeReferent()+"</font></b>"), MyParagraph(style='style3', text=u"<b>ALE : <font color=black>"+self.bilanView.ALEnom()+"</font></b>")],
                        [MyParagraph(style='style3', text=u"<b>Inscrit à ALE de: <font color=black>"+self.bilanView.incritALE()+"</font></b>"), MyParagraph(style='style3', text=u"<b>Tél : <font color=black>"+self.bilanView.refTel()+"</font></b>"), MyParagraph(style='style3', text=u"<b>Tél : <font color=black>"+self.bilanView.ALEtel()+"</font></b>")],
                        [MyParagraph(style='style3', text=u"<b>Tél : <font color=black>"+self.bilanView.LCtel()+"</font></b>"), MyParagraph(style='style3', text=u"<b>Mel : <font color=black>"+self.bilanView.refMail()+"</font></b>"), MyParagraph(style='style3', text=u"<b>Mel : <font color=black>"+self.bilanView.ALEmail()+"</font></b>")],
                        [MyParagraph(style='style3', text=u"<b>Mel : <font color=black>"+self.bilanView.LCmail()+"</font></b>"), None, None],                        
                        ]
        tableau = Table(data=tableau_data, style=style_tableau)
        self.story.append(tableau)
    
    def situation_fin_acc_intro(self):
        self.story.append(MyParagraph(style='style1', text=u"<b>Situation à la fin de l'accompagnement :</b>", spaceAfter=5))
        
    def sit_emploi(self):
        self.story.append(MyParagraph(u"<b>Emploi</b>", 'bullet-style3', bulletText='-'))
        self.story.append(MyParagraph(style='style_base', text=u"Poste occupé : <b>"+self.bilanView.postOcc()+u"</b>..... Code ROME : <b>"+self.bilanView.rom()+"</b>...Type de contrat : <b>"+self.bilanView.typecontrat()+"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Durée du <b>"+self.bilanView.empldeb()+u"</b>...au <b>"+self.bilanView.emplfin()+u"</b>..... Durée hebdomadaire : .....<b>"+self.bilanView.dureehebd()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Nom et adresse de l'entreprise : ....<b>"+self.bilanView.emplcoord()+u"</b>", spaceAfter=7))
        
    def sit_formation(self):
        self.story.append(MyParagraph(u"<b>Formation</b>", 'bullet-style3', bulletText='-'))
        self.story.append(MyParagraph(style='style_base', text=u"Intitulé : <b>"+self.bilanView.formint()+u"</b>..... Nom et coordonnées de l'Organisme : <b>"+self.bilanView.formcoor()+u"</b> ....."))
        self.story.append(MyParagraph(style='style_base', text=u"Objectif : <b>"+self.bilanView.formobj()+u"</b>..... Nombre d’heures: <b>"+self.bilanView.formheures()+u"</b> ....."))
        self.story.append(MyParagraph(style='style_base', text=u"Date d'entrée en stage : <b>"+self.bilanView.formentre()+u"</b>..... au <b>"+self.bilanView.formsortie()+u"</b> .....", spaceAfter=5))

    def sit_entr(self):
        self.story.append(MyParagraph(u"<b>Création d'entreprise</b>", 'bullet-style3', bulletText='-'))
        self.story.append(MyParagraph(style='style_base', text=u"Nature du projet : <b>"+self.bilanView.entrproj()+u"</b>....."))
        self.story.append(MyParagraph(style='style_base', text=u"Lieu : <b>"+self.bilanView.entrlieu()+u"</b>.....A compter du <b>"+self.bilanView.entrdate()+"</b>..."))
        self.story.append(MyParagraph(style='style_base', text=u"Justificatif : "))
        self.story.append(MyParagraph(style='style_base', text=u"<b>"+self.bilanView.entrjusti()+u"</b>"))
        
    def sit_rech(self):
        self.story.append(MyParagraph(u"<b>Toujours à la recherche d'un emploi</b>", 'bullet-style3', bulletText='-'))                
        self.story.append(MyParagraph(style='style_base', text=u"Intitulés des emplois/métiers recherchés : <b>"+self.bilanView.rech_int()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Code ROME : <b>"+self.bilanView.rech_rome()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Secteurs d'activité : <b>"+self.bilanView.rech_act()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Zones géographiques : <b>"+self.bilanView.rech_zones()+u"</b>", spaceAfter=5))
        
    def sit_cess(self):
        self.story.append(MyParagraph(u"<b>Cessation d'inscription</b>", 'bullet-style3', bulletText='-'))
        self.story.append(MyParagraph(style='style_base', text=u"A compter du : <b>"+self.bilanView.cess_date()+u"</b>... Préciser le motif : <b>"+self.bilanView.cess_motif()+"</b>", spaceAfter=7))     
        
    def situation_fin_acc(self):
        self. situation_fin_acc_intro()
        self.sit_emploi()
        self.sit_formation()
        self.sit_entr()
        self.sit_rech()
        self.sit_cess()
    
    def _persoAllEvents(self):
        events = self.bilanView.persoAllEvents()
        results = []
        for event in events:
            tmpList = []
            for case in event:
                tmpList.append(MyParagraph(unicode(case), 'style_base'))
            results.append(tmpList)
        return results 
    
    def action_solutions(self):
        self.story.append(MyParagraph(u"<b>Recherche de solutions pour les difficultés sociales et personnelles</b>", 'bullet-style3', bulletText='-', spaceAfter=20))
        table_data = [[u"Dates", u"Institutions/organismes solicités", u"Action réalisées", u"Résultats"]]+self._persoAllEvents()
        self.story.append(styleGetter.getTableau(data=table_data, spaceAfter=15))
        
    def action_stab(self):
        self.append(style='bullet-style3', text=u"<b>Stabilisation du ou des métiers recherchés / Elaboration du projet professionnel</b>", bulletText='-')
        self.append(style='style_base', text=u"<i>(A détailler par rapport aux fiches ROME des emplois recherchés)</i>", spaceAfter=5)
        self.append(style='style_base', text=u"<b>Compétences acquises et transférables : </b>" + self.bilanView.action_comp())
        self.append(style='style_base', text=u"<b>Capacités cognitives : </b>" + self.bilanView.action_cogn())
        self.append(style='style_base', text=u"<b>Capacités relationnelles : </b>" + self.bilanView.action_rela(), spaceAfter=5)
        
        
        
    def action_periodEntr_aux(self, number):
        self.story.append(MyParagraph(style='style_base', text=u"Du <b>"+self.bilanView.action_P_deb(number)+u"</b> au <b>"+self.bilanView.action_P_fin(number)+u"</b> Nom et adresse de l'entreprise n°"+str(number)+u": <b>"+self.bilanView.action_P_coord(number)+u"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Résultat (pistes dégagées) : <b>"+self.bilanView.action_P_res(number)+"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Compétences à acquérir: <b>"+self.bilanView.action_P_comp(number)+"</b>", spaceAfter=7))
        
    def action_periodEntr(self):
        self.story.append(MyParagraph(style='style_base', text=u"<b>Période(s) en entreprise</b>"))
        self.action_periodEntr_aux(1)
        self.action_periodEntr_aux(2)
    
    def _emploiAllEvents(self):
        events = self.bilanView.emploiAllEvents()
        results = []
        for event in events:
            tmpList = []
            for case in event:
                tmpList.append(MyParagraph(unicode(case), 'style_base'))
            results.append(tmpList)
        return results 
    
    def action_EmplAction(self):
        table_data = [[u"Dates", u"Entreprises contactées", u"Modalités", u"Résultats obtenus"]]+self._emploiAllEvents()
        return styleGetter.getTableau(data=table_data, spaceAfter = 15)
    
    def action_accEmpl(self):
        self.story.append(MyParagraph(u"<b>Accompagnement vers l'emploi / pistes d'emploi</b>", 
                                      'bullet-style3', spaceAfter=5, bulletText='-'))
        self.story.append(MyParagraph(style='style_base', 
                                      text=u"Nombre d’OE correspondant à l’emploi recherché : <b>" \
                                            +self.bilanView.action_nbOE()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', 
                                      text=u"Nombre de candidatures sur ces offres : <b>"\
                                           +self.bilanView.action_nbCa()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', 
                                      text=u"Nombre d’entretiens d’embauche obtenus : <b>"\
                                           +self.bilanView.action_nbEN()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', 
                                      text=u"Autres emplois recherchés (nom des emplois "\
                                           +"(codes ROME -----   -----  -----) : <b>"\
                                           +self.bilanView.action_autreEmp()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', 
                                      text=u"Autres secteurs professionnels : <b>"\
                                           +self.bilanView.action_autreSect()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', 
                                      text=u"Autres activités : <b>"\
                                            +self.bilanView.action_autreAct()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', 
                                      text=u"Secteurs géographiques : <b>"\
                                           +self.bilanView.action_sect()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', 
                                      text=u"Actions réalisées pendant votre accompagnement", 
                                      spaceAfter=7))
        self.story.append(self.action_EmplAction())
        
    
    def action_suivi(self):
        self.story.append(MyParagraph(u"<b>Suivi dans l'emploi</b>", 'bullet-style3', bulletText='-'))
        self.story.append(MyParagraph(style='style_base', text=u"Contexte général de votre reprise d’emploi : <b>"+self.bilanView.action_reprCont()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Difficultés rencontrées : <b>"+self.bilanView.action_reprDiff()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Réponses apportées : <b>"+self.bilanView.action_reprRep()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Nombre d’entretiens de suivis : <b>"+self.bilanView.action_reprEntr()+u"</b>"))
        self.story.append(MyParagraph(style='style_base', text=u"Modalités (déplacement demandeur d’emploi/référent/ téléphone…) : <b>"+self.bilanView.action_reprMod()+u"</b>", spaceAfter=10))
        
    
    def actionpdt(self):
        self.story.append(MyParagraph(style='style1', text=u"<b>Actions réalisées pendant votre accompagnement : </b>", spaceAfter=5))
        self.action_solutions()
        self.action_stab()
        self.action_periodEntr()
        self.action_accEmpl()
        self.action_suivi()
    
    def lesactionsPrio_aux(self):
        actions = self.bilanView.lesactionsPrio()
        result = []
        for action in actions:
            result.append([MyParagraph(style='style_base', text=item) for item in action])
        return result
        
    def lesactionsPrio(self):
        table_data = [[u"Dates", u"Actions", u"Démarches à effectuer"]]+self.lesactionsPrio_aux()
        return styleGetter.getTableau(data=table_data, spaceAfter = 15)
        
    def actionprio(self):
        self.story.append(MyParagraph(style='style1', text=u"<b>Actions prioritaires à mener à l’issue de la prestation</b>", spaceAfter=5))
        self.story.append(MyParagraph(style='style2', text=u"<i><b>Pour les personnes n’ayant pas trouvé de solutions (emploi/formation/création d’entreprise…)</b></i>", spaceAfter=5))
        self.story.append(self.lesactionsPrio())
        
    def obsRef(self):
        self.story.append(MyParagraph(style='style1', text=u"<b>Observations du référent</b>", spaceAfter=5))
        self.append(style='style_base', text=self.bilanView.conc_obsref(), spaceAfter=0)
        
    def obsBen(self):
        self.story.append(MyParagraph(style='style1', text=u"<b>Observations du bénéficiaire</b>", spaceAfter=5))
        self.story.append(MyParagraph(style='style_base', text=self.bilanView.conc_obsbene(), spaceAfter=7))
        
    def conc(self):
        self.story.append(MyParagraph(style='style3', text=u"Date de suivi à 3 mois : <b><font color=black>"+self.bilanView.conc_datesuivi()+"</font></b>"))
        self.story.append(MyParagraph(style='style3', text=u"Conseiller prescripteur (Nom, Prénom, ALE) : <b><font color=black>"+self.bilanView.conc_cons()+"</font></b>"))
        self.story.append(MyParagraph(style='style3', text=u"Date de rendez vous avec le conseiller prescripteur à l’issue du bilan : <b><font color=black>"+self.bilanView.conc_datenext()+"</font></b>"))
        self.story.append(MyParagraph(style='style3', text=u"Date de réalisation du bilan : <b><font color=black>"+self.bilanView.conc_date()+"</font></b>", spaceAfter=10))
        
    def pdp(self):
        self.story.append(MyParagraph("<b>Signature du bénéficiaire</b>", 'style4', firstLineIndent=10))
        self.story.append(MyParagraph("<b>Signature du référent et cachet de l'organisme</b>", 'style4', rightIndent = 50, spaceAfter = 50, alignment = TA_RIGHT))
        self.story.append(MyParagraph("<b>Feuillet 1 : à remettre au bénéficiaire  - Feuillet 2 : à transmettre au conseiller prescripteur de l’ANPE - Feuillet 3 : à conserver par le référent </b>", 'style5', alignment = TA_CENTER))
    
    def buildDoc(self):
        self.entete()
        self.head()
        self.intro()
        self.tableau_intro()
        self.situation_fin_acc()
        self.actionpdt()
        self.actionprio()
        self.obsRef()
        self.obsBen()
        self.conc()
        self.pdp()
        self.doctemplate.build(self.story)
        #self.doctemplate.multiBuild(self.story)












