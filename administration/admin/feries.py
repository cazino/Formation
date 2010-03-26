# -*- coding: utf-8 -*-
from datetime import date, timedelta

class Feries(object):
    
    def __init__(self, year=date.today().year):
        self.year = year
        
    def paques(self):
        """
        Paques(an): trouve la date de Pâques d'une année donnée an
        """
        an = self.year
        a=an//100
        b=an%100
        c=(3*(a+25))//4
        d=(3*(a+25))%4
        e=(8*(a+11))//25
        f=(5*a+b)%19
        g=(19*f+c-e)%30
        h=(f+11*g)//319
        j=(60*(5-d)+b)//4
        k=(60*(5-d)+b)%4
        m=(2*j-k-g+h)%7
        n=(g-h+m+114)//31
        p=(g-h+m+114)%31
        jour=p+1
        mois=n
        return date(day=jour, month=mois, year=an)
 
    def paques_oudin(self):
        
        g = self.year % 19
        c = self.year // 100
        c_4 = c // 4
        e = (8 * c + 13) // 25
        h = (19 * g + c - c_4 - e + 15) % 30
        k = h // 28
        p = 29 // (h + 1)
        q = (21 - g) // 11
        i = (k * p * q - 1) * k + h
        b = self.year // 4 + self.year
        j1 = b + i + 2 + c_4 - c
        j2 = j1 %7
        r = 28 + i - j2 # Original formula
        if r <= 31:
            return date(day=r, month=03, year=self.year) + timedelta(days=1) # Because on veut le lundi de paques et pas le dimanche
        return date(day=(r - 31), month=04, year=self.year) + timedelta(days=1)
    
    def feries(self):
        paques = self.paques_oudin()
        ascension = paques + timedelta(days=38)
        pentecote = paques + timedelta(days=49)
        return [date(day=1, month=1, year=self.year),   # Jour de l'an
                paques,                                 # Paques                  
                date(day=1, month=5, year=self.year),   # Fete du travail
                date(day=8, month=5, year=self.year),   # Armistice
                ascension,                              # Ascension
                pentecote,                              # Pentecote 
                date(day=14, month=7, year=self.year),  # Fete nationale
                date(day=15, month=8, year=self.year),  # Assomption
                date(day=1, month=11, year=self.year),  # Toussaint
                date(day=11, month=11, year=self.year), #Armistice
                date(day=25, month=12, year=self.year), # Noel
                ]
    
def _feries_list(last_date, new_date):
    if last_date.year != new_date.year:
        return Feries(last_date.year).feries() + Feries(new_date.year).feries()
    return  Feries(last_date.year).feries()
    
def intervalle(last_date, new_date):
    # Nombre de jours entre deux dates à l'exclusion des jours fêriés qui tombent en semaine 
    feries_list = _feries_list(last_date, new_date)
    nb_non_counting_days = len([jour for jour in feries_list if last_date <= jour and jour <= new_date
                                                             and 1 <= jour.isoweekday()
                                                             and jour.isoweekday() <= 5])
    return (new_date - last_date).days - nb_non_counting_days  











