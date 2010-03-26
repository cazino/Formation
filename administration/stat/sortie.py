# -*- coding: utf-8 -*-
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import ParagraphStyle, PropertySet
from reportlab.lib.colors import black, darkred
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from calcul import SiteCalc

class StatStyleSheet(object):
    
    @classmethod
    def get(self, style_name, **kw):
        if style_name == 'style1':
            return ParagraphStyle(name='style1', fontName='helvetica', fontSize=16, textColor=black, **kw)
        if style_name == 'style1-right':
            return ParagraphStyle(name='style1-right', parent=MyStyleSheet.get('style1'), leftIndent = 315, **kw)
        if style_name == 'style2':
            return ParagraphStyle(name='style2', fontName='helvetica', fontSize=12, textColor=black, **kw)
        if style_name == 'style3':
            return ParagraphStyle(name='style3', fontName='helvetica', fontSize=10, textColor=black, **kw)

class StatParagraph(Paragraph):
    
    def __init__(self, text, style, **kw):
        Paragraph.__init__(self, text, style=StatStyleSheet.get(style, **kw))
        
        
class StatView(object):
    
    date_format = '%d/%m/%Y'
    
    def __init__(self, stat):
        self.stat = stat
        self.result = SiteCalc(self.stat.site, self.stat.debut, self.stat.fin).calculate() 
    def site(self):
        return self.stat.site
    
    def date_debut(self):
        return self.stat.debut.strftime(StatView.date_format)
    
    def date_fin(self):
        return self.stat.fin.strftime(StatView.date_format)
    
    def stat_result_list(self):
        return self.result[0].to_list()
    
    def frein_result_list(self):
        return self.result[1].to_list()
    
    def nb_lc(self):
        return self.result[2]

class StatDoc(object):

    def __init__(self, response, stat):
        self.stat_view = StatView(stat)
        self.doctemplate = SimpleDocTemplate(response, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        self.story = []
        
    def title(self):
        self.story.append(StatParagraph(u"<b><i>Statistiques</b></i>", 'style1', alignment=TA_CENTER, spaceAfter=50))
        
    def infos_gen(self):
        self.story.append(StatParagraph(u"<b><i>Site : </b></i> %s" % (self.stat_view.site()), 'style2', spaceAfter=15))
        self.story.append(StatParagraph(u"<b><i>Période : </b></i> du %s au %s" 
                                        % (self.stat_view.date_debut(), self.stat_view.date_fin()),
                                         'style2', spaceAfter=15))
        self.story.append(StatParagraph(u"<b><i>Nombre de lettres de commandes considérées : </b></i>%s" 
                                        % (self.stat_view.nb_lc(),),
                                         'style2', spaceAfter=30))
        
    def stat_result(self):
        self.story.append(StatParagraph(u"<b><i><u>Pemier RDV et abandon </u></i></b>", 'style2', spaceAfter=15))
        for (categorie, resultat) in self.stat_view.stat_result_list():
            self.story.append(StatParagraph(u"<b><i>%s : </b></i>%s" % (categorie, resultat), 'style3', spaceAfter=15))
    
    def frein_type_result(self, frein_type, resultat_list):
        en_tete = ((StatParagraph("<b><i>" + frein_type + "</i></b>", 'style3'),
                    StatParagraph("<b><i>" + u"Frein le plus important" + "</i></b>", 'style3'),
                    StatParagraph("<b><i>" + u"Frein présent" + "</i></b>", 'style3')),)
        data = tuple([(StatParagraph(categorie, 'style3'),
                       StatParagraph(str(nb_plus_imp), 'style3'),
                       StatParagraph(str(nb_all), 'style3'))
                       for (categorie, nb_plus_imp, nb_all) in resultat_list])
        table_data = en_tete + data
        table_style = TableStyle([('GRID', (0,0), (-1,-1), 0.25, black),])
        table_style.spaceAfter=25
        table_style.spaceBefore=25
        self.story.append(Table(data=table_data, style=table_style))
        
    def frein_result(self):
        self.story.append(StatParagraph(u"<b><i><u>Freins à l'emploi</u></i></b>", 'style2', spaceBefore=30, spaceAfter=15))
        for (frein_type, resultat_list) in self.stat_view.frein_result_list():
            self.frein_type_result(frein_type, resultat_list)
        
    def build_doc(self):
        self.title()
        self.infos_gen()
        self.stat_result()
        self.frein_result()
        self.doctemplate.build(self.story)
  

