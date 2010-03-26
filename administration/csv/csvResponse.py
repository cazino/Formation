# -*- coding: utf-8 -*-
import csv, datetime, calendar
from greta.administration.models import models_etat


def compare(a, b):
    (key1,(order1, item1)) = a
    (key2,(order2, item2)) = b
    return order1-order2

def writeResponse(request, queryset, response):
    writer = csv.writer(response, delimiter="\t")
    for index, lc in enumerate(queryset.filter(avancement=models_etat.LC_EN_COURS)):
        lc_csvView = csvView(lc, datetime.datetime.today().date())
        viewData = lc_csvView.csvDict().items()
        viewData.sort(cmp=compare)
        if index==0:
            columnNames = [a for (a, (b, c)) in viewData]
            writer.writerow(columnNames)
        lc_data = [c for (a, (b, c)) in viewData]
        writer.writerow(lc_data)
    return response


class csvView(object):

    date_format = "%d/%m/%Y"
    
    def __init__(self, lc, referenceDay):
        self.lc = lc
        self.referenceDay = referenceDay 
        self.yearBefore = referenceDay.year-1
        self.lastDay = self.__init_lastDay()
        self.period = period(self.lc.date_debut, self.lastDay)
        self.entreenpresta = self.lc.avancement==models_etat.LC_EN_COURS or self.lc.avancement==models_etat.LC_CLOTURE
        
    def presta(self):
        if self.entreenpresta:
            return 1
        return 2 

    def __init_lastDay(self):
        fin_lc = self.lc.lastDayPresta()
        if fin_lc and fin_lc<self.referenceDay:
            return fin_lc
        return  self.referenceDay
    
    def daysUsedYearbefore(self):
        if self.entreenpresta:
            firstday = datetime.date(day=1, month=1, year=self.yearBefore)
            lastday = datetime.date(day=31, month=12, year=self.yearBefore)
            return period(firstday, lastday).intersection(self.period).days
        return 0
        
        
    def daysUsedMonth(self, month):
        if self.entreenpresta:
            firstday = datetime.date(day=1, month=month, year=self.referenceDay.year)
            lastday = datetime.date(day=calendar.monthrange(month=month, year=self.referenceDay.year)[1], month=month, year=self.referenceDay.year)
            return period(firstday, lastday).intersection(self.period).days
        return 0

    def nbJours(self):
        if self.entreenpresta:
            return (self.lastDay-self.lc.date_debut).days+1
        return 0
            
    def montant_facturable(self):
        if self.entreenpresta:
            return self.lc.marche.montantjour()*self.nbJours()
        return 0
        
    def csvDict(self):
        resultDict = {'NUM LC': (0,self.lc.numero_lc),
                      'NUM CONVENTION': (1, self.lc.marche.polemploi_id),
                      'DATE ENTREE': (2, self.lc.date_debut.strftime(self.date_format)),
                      'DATE SORTIE': (3, self.lc.date_fin.strftime(self.date_format)),
                      'MONTANT LC': (4, self.lc.marche.montant_unitaire),
                      'CIVILITE': (5, self.lc.civilite),
                      'NOM': (6, self.lc.nom),
                      'PRENOM': (7, self.lc.prenom),
                      'IDENTIFIANT': (8, self.lc.polemploi_id),
                      'ALE': (9, self.lc.ale_prescriptrice),
                      'PRESTATAIRE': (10, self.lc.site.prestataire.nom),
                      'MVEG OU MVEP': (11, self.lc.mv),
                      'SITE': (12, self.lc.site.nom),
                      'ENTREE EN PRESTATION': (13, self.presta()),
                      'REFERENT': (14, self.lc.charge_insertion.nom),
                      str(self.yearBefore): (15, self.daysUsedYearbefore()),
                      'JANVIER': (16, self.daysUsedMonth(1)),
                      'FEVRIER': (17, self.daysUsedMonth(2)),
                      'MARS': (18, self.daysUsedMonth(3)),
                      'AVRIL': (19, self.daysUsedMonth(4)),
                      'MAI': (20, self.daysUsedMonth(5)),
                      'JUIN': (21, self.daysUsedMonth(6)),
                      'JUILLET': (22, self.daysUsedMonth(7)),
                      'AOUT': (23, self.daysUsedMonth(8)),
                      'SEPTEMBRE': (24, self.daysUsedMonth(9)),
                      'OCTOBRE': (25, self.daysUsedMonth(10)),
                      'NOVEMBRE': (26, self.daysUsedMonth(11)),
                      'DECEMBRE': (27, self.daysUsedMonth(12)),
                      'NB DE JOURS': (28, self.nbJours()),
                      'DATE SORTIE REELLE': (29, self.lc.lastDayPresta()),
                      'MONTANT FACTURABLE': (30, self.montant_facturable()),   
                      }
        return resultDict
    
    
class period(object):
    
    def __init__(self, date1, date2):
        self.deb = min([date1, date2])
        self.fin = max([date1, date2])
        
    def disjoin(self, period):
        return self.fin<period.deb or period.fin<self.deb
            
    def intersection(self, period):
        if self.disjoin(period):
            return datetime.timedelta()
        else:
            date_list=[self.deb, self.fin, period.deb, period.fin]
            date_list.remove(max(date_list))
            date_list.remove(min(date_list))
            return max(date_list)-min(date_list)+datetime.timedelta(days=1)
        
        
        