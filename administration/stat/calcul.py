# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from greta.administration.models import Frein, ouvertureRdv, models_etat


class StatResult(object):
    
    attributs = [('premier_rdv_absent', u"Premier RDV - Absent"),
                 ('premier_rdv_report', u"Premier RDV - Report"),
                 ('premier_rdv_pnc', u"Premier RDV - Présent non contractualisé"),
                 ('premier_rdv_pc', u"Premier RDV - Présent contractualisé"),
                 ('abandon_1', u"Abandon - 1 mois"),
                 ('abandon_2', u"Abandon - 2 mois"),
                 ('abandon_3', u"Abandon - 3 mois"),
                 ('abandon_4', u"Abandon - 4 mois"),
                 ('abandon_5', u"Abandon - 5 mois"),
                 ('abandon_6', u"Abandon - 6 mois")]
                        
    def __init__(self):
        for (attribut, desc) in StatResult.attributs:
            setattr(self, attribut, 0)
            
    def __repr__(self):
        return ','.join([str((attribut, getattr(self, attribut))) 
                         for (attribut, desc) in StatResult.attributs])
            
    def __eq__(self, other):
        bool_list = [getattr(self, attribut) == getattr(other, attribut) 
                     for (attribut, desc) in StatResult.attributs] 
        for bolean in bool_list:
            if not bolean:
                 return False
        return True

    def __add__(self, other):
        result = StatResult()
        for (attribut, desc) in StatResult.attributs:
            setattr(result, attribut, getattr(self, attribut) + getattr(other, attribut))
        return result

    def to_list(self):
        return [(desc, getattr(self, attribut)) for (attribut, desc) in StatResult.attributs]

class FreinResult(object):
    
    def __init__(self, frein, valeurs_frein):
        self.frein = frein # Frein professionnels, ou familiaux ....
        self.valeurs_frein =  valeurs_frein
        self.first_frein = dict([(valeur, 0) for valeur in self.valeurs_frein])
        self.all_frein = dict([(valeur, 0) for valeur in self.valeurs_frein])
        
    def __repr__(self):
        return "<greta.administration.stat.stat.FreinResult frein=%s first_frein=%s all_frein=%s>" \
                % (self.frein, self.first_frein, self.all_frein)
        
    def __eq__(self, other):
        return self.first_frein == other.first_frein\
         and self.all_frein == other.all_frein
         
    def __add__(self, other):
        result = FreinResult(self.frein, self.valeurs_frein)
        result.first_frein = self. _dict_add(self.first_frein, other.first_frein)
        result.all_frein = self. _dict_add(self.all_frein, other.all_frein)
        return result
    
    def add(self, valeur_frein):
       self.all_frein[valeur_frein] += 1
       
    def add_first(self, valeur_frein):
        self.first_frein[valeur_frein] += 1
        self.all_frein[valeur_frein] += 1
    
    def _dict_add(self, dict1, dict2):
        # Addition de deux dictionnaires
        # {x : 2} + {x : 1, y : 1} = {x : 3, y : 1}
        result = {}
        key_value_list = dict1.items() + dict2.items()
        for (key, value) in key_value_list:
            result.setdefault(key, 0)
            result[key] += value
        return result
    
    def to_list(self):
        return [(valeur, self.first_frein[valeur], self.all_frein[valeur]) for valeur in self.valeurs_frein]
    
class LCFreinResult(object):
    
    def __init__(self):
        self.frein_result_dic = dict([(frein, FreinResult(frein, valeur_frein)) 
                      for (frein, valeur_frein) in Frein.freins_dic.items()])
        
    def __repr__(self):
        return "<greta.administration.stat.stat.LCFreinResult %s>" % self.frein_result_dic
    
    def __eq__(self, other):
        return self.frein_result_dic == other.frein_result_dic
    
    def __add__(self, other):
        result = LCFreinResult()
        for frein in self.frein_result_dic.keys():
            result.frein_result_dic[frein] = self.frein_result_dic[frein] + other.frein_result_dic[frein]
        return result
         
    def add(self, categorie, value):
        self.frein_result_dic[categorie].all_frein[value] += 1
        
    def add_first(self, categorie, value):
        self.frein_result_dic[categorie].first_frein[value] += 1
        self.frein_result_dic[categorie].all_frein[value] += 1

    def to_list(self):
        return [(frein, frein_result.to_list()) for (frein, frein_result) in self.frein_result_dic.items()]
        
                      
class LCFreinCalc(object):

    def __init__(self, lc):
        self.lc = lc
        
    def calculate(self):
        result = LCFreinResult()
        try:
            frein = self.lc.frein
            cat_fields = [(Frein.PRO_INTIT, 'pro'), (Frein.PERSO_INTIT, 'perso'),
                      (Frein.SOCIO_INTIT, 'socio'), (Frein.EMPL_INTIT, 'empl')]
            for (cat, field_name) in cat_fields:
                for field_postfix in range(1, 4):
                    full_field_name = "%s%s" % (field_name, field_postfix)
                    frein_value = getattr(frein, full_field_name)
                    if frein_value:
                        if field_postfix == 1:
                            result.add_first(cat, frein_value)
                        else:
                            result.add(cat, frein_value)     
            return result
        except ObjectDoesNotExist:
            pass
        return result 


class LCStatCalc(object):
    
    def __init__(self, lc):
        self.lc = lc
        self.result = StatResult()
        
    def _ouverture(self):
        try:
            statut = self.lc.ouverture_rdv.statut 
            if  statut == ouvertureRdv.ABSENT:
                self.result.premier_rdv_absent = 1
            elif statut == ouvertureRdv.REPORT:
                self.result.premier_rdv_report = 1
            elif statut == ouvertureRdv.PRESENT_NC:
                self.result.premier_rdv_pnc = 1
            elif statut == ouvertureRdv.PRESENT_C:
                self.result.premier_rdv_pc = 1
        except ObjectDoesNotExist:
            pass
        
    def _abandon(self):
        if self.lc.abandon:
            date_fin = self.lc.lastDayPresta()
            mois_abandon = ((date_fin - self.lc.date_debut).days // 30) + 1 
            if mois_abandon > 6:
                mois_abandon = 6
            attribut = "abandon_%s" % (mois_abandon,)
            setattr(self.result, attribut, 1)
            
    def calculate(self):
        self._ouverture()
        self._abandon()
        return self.result
        
        
class SiteCalc(object):
    
    def __init__(self, site, date_debut, date_fin):
        self.site = site
        self.date_debut = date_debut
        self.date_fin = date_fin 
        
    def calculate(self):
        result_list = [(LCStatCalc(lc).calculate(), LCFreinCalc(lc).calculate()) for lc 
                            in self.site.lettrecommande_set.exclude(avancement__exact=models_etat.LC_EN_ATTENTE)
                            .filter(date_debut__gte=self.date_debut)
                            .filter(date_debut__lte=self.date_fin)]
        final_stat_result = StatResult()
        final_frein_result = LCFreinResult()
        for (stat_result,frein_result)  in result_list:
            final_stat_result += stat_result
            final_frein_result += frein_result 
        return (final_stat_result,final_frein_result, len(result_list))          
        
        
