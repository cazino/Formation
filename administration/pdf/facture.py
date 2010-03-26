# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from greta.administration.models import LettreCommande
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import ParagraphStyle, PropertySet, StyleSheet1
from reportlab.lib.colors import black, darkred
from reportlab.lib.enums import TA_CENTER, TA_RIGHT 
from gretaview import GretaView
import common
from pynum2word import num2word_FR
import datetime




        

class FactureView(GretaView):
    
    def __init__(self, lc):
        self.lc = lc

    def ale(self):
        return self.lc.ale_prescriptrice
        
    def numero_marche(self):
        return self.lc.marche.polemploi_id
    
    def numero_lc(self):
        return self.lc.numero_lc

    def date_debut(self):
        return self.lc.date_debut.strftime(common.date_format)
    
    def date_fin(self):
        return self.lc.date_fin.strftime(common.date_format)
    
    def lastDayPresta(self):
        return self.lc.lastDayPresta().strftime(common.date_format)
    
    def nom_prenom(self):
        prefix = None
        if self.lc.civilite == 1:
            prefix = u"MONSIEUR"
        if self.lc.civilite == 2:
            prefix = u"MADAME"
        return u" ".join([prefix, self.lc.nom.upper(), self.lc.prenom.upper()])
    
    def jours_prestation(self):
        return (self.lc.lastDayPresta() - self.lc.date_debut).days + 1
    
    def jours_prestation_string(self):
        return str(self.jours_prestation())
    
    def montant_presta(self):
        return self.lc.marche.montantjour() * self.jours_prestation()
    
    def montant_presta_entier(self):
        return int(abs(self.montant_presta()))
    
    def montant_presta_decimal(self):
        return  int(("%.2f" % self.montant_presta()).split('.')[1])
    
    def montant_presta_entier_word(self):
        return num2word_FR.Num2Word_FR().to_cardinal(self.montant_presta_entier())
        
    
    def montant_presta_decimal_word(self):
        return unicode(num2word_FR.Num2Word_FR().to_cardinal(self.montant_presta_decimal()), encoding='latin-1')
        #return 'aaa'
    
    def montant_presta_word(self):
        return unicode(self.montant_presta_entier_word()) + u" Euros " + unicode(self.montant_presta_decimal_word()) + u" Centimes"
    
    def lieudate(self):
        return datetime.date.today().strftime(common.date_format)
    
class MyStyleSheet(object):
    
    def get(self, style_name, **kw):
        if style_name == 'style1':
            return ParagraphStyle(name='style1', fontName='helvetica', fontSize=12, textColor=black, **kw)
        if style_name == 'style1-right':
            return ParagraphStyle(name='style1-right', parent=MyStyleSheet.get('style1'), leftIndent = 315, **kw)
        if style_name == 'style2':
            return ParagraphStyle(name='style2', fontName='helvetica', fontSize=10, textColor=black, **kw)
    get = classmethod(get)    


class myParagraph(Paragraph):
    
    def __init__(self, text, style, **kw):
        Paragraph.__init__(self, text, style=MyStyleSheet.get(style, **kw))
        
class FactureDoc(object):
        
    def __init__(self, response, lc):
        self.facture_view = FactureView(lc) 
        self.doctemplate = SimpleDocTemplate(response, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        self.story = []
        
    def destinataire(self):
        self.story.append(myParagraph(u"POLE EMPLOI", 'style1-right'))
        self.story.append(myParagraph(u"Direction Régionale IDF", 'style1-right'))
        self.story.append(myParagraph(u"Agence comptable PRESTATIONS", 'style1-right'))
        self.story.append(myParagraph(u"1, place J B Clément", 'style1-right'))
        self.story.append(myParagraph(u"93192  NOISY LE GRAND", 'style1-right', spaceAfter=60))
        
    def siret(self):
        self.story.append(myParagraph(u"N° SIRET : 19930122700021", 'style2', leftIndent=50, spaceAfter=30))
        
    def titre(self):
        self.story.append(myParagraph(u"<b><i><u>Facture</u></i></b>", 'style1', alignment=TA_CENTER, spaceAfter=30))
        
    def first_paragraph(self):
        #self.story.append(myParagraph(u"<b>Marché n° 06/M000562 du 01/12/2006 Lot n°2</b>", 'style1'))
        self.story.append(myParagraph(u"<b>Marché "+self.facture_view.numero_marche()+"</b>", 'style1'))
        self.story.append(myParagraph(u"« Mobilisation vers l’emploi »", 'style1'))
        self.story.append(myParagraph(u"POLE EMPLOI "+self.facture_view.ale().upper(), 'style1'))
        #self.story.append(myParagraph(u"MARCHE M0059", 'style1'))
        self.story.append(myParagraph(u"Lettre de commande n° <b>"+self.facture_view.numero_lc()+u"</b> DU <b>"+self.facture_view.date_debut()+u"</b> AU <b>"+self.facture_view.date_fin()+u"</b>", 'style1'))
        self.story.append(myParagraph(u"Date de sortie : <b>" + self.facture_view.lastDayPresta() + u"</b>", 'style1', spaceAfter=10))
         
    def second_paragraph(self):    
        self.story.append(myParagraph(u"Nom du bénéficiaire : <b>" + self.facture_view.nom_prenom() + u"</b>", 'style1', spaceAfter=10))
        self.story.append(myParagraph(u"Montant de la prestation", 'style1'))
        self.story.append(myParagraph(u"<b>(" + self.facture_view.jours_prestation_string() + u")</b> Jours....................................<b>%.2f " % (self.facture_view.montant_presta()) + u"</b>€uros", 'style1', spaceAfter=25))
        self.story.append(myParagraph(u"Arrêtée et certifiée conforme la présente facture à la somme de :", 'style1', spaceAfter=25))
        
        table_style = TableStyle([('BOX', (0,0), (-1,-1), 0.25, black),
                                  ('BOX', (0,0), (-1,-1), 0.25, black),])
        table_style.spaceAfter=25
        table_data = [[myParagraph(u"<b>" + self.facture_view.montant_presta_word().upper() + u"</b>", 'style1', alignment=TA_CENTER),],]               
        self.story.append(Table(data=table_data, style=table_style))
        
    def third_paragraph(self):
        self.story.append(myParagraph(u"Montant non assujetti à la TVA", 'style1', spaceAfter=15))
        self.story.append(myParagraph(u"Règlement à établir à l'ordre de :", 'style1'))
        self.story.append(myParagraph(u"<b>L’Agent Comptable du Lycée Condorcet 31, rue Désiré Chevalier 93100 Montreuil s/Bois.</b>", 'style1', spaceAfter=15))
        self.story.append(myParagraph(u"<u><b>REFERENCES BANCAIRES : </b></u>", 'style1', spaceAfter=5))
        self.story.append(myParagraph(u"- Institution Bancaire : <b>TP Bobigny</b>", 'style1'))
        self.story.append(myParagraph(u"- N° de compte : <b>00001001426</b>", 'style1'))
        self.story.append(myParagraph(u"- Code guichet : <b>93000</b>", 'style1'))
        self.story.append(myParagraph(u"- Clé : <b>21</b>", 'style1', spaceAfter=30))
        self.story.append(myParagraph(u"Fait à Neuilly sur Marne, le " + self.facture_view.lieudate(), 'style1', alignment=TA_RIGHT, rightIndent=15))
        
        
        
    def buildDoc(self):
        self.destinataire()
        self.siret()
        self.titre()
        self.first_paragraph()
        self.second_paragraph()
        self.third_paragraph()
        self.doctemplate.build(self.story)












