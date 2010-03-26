# -*- coding: utf-8 -*-
from django.test import TestCase
from administration.models import LettreCommande, Prestataire, Site, ChargeInsertion, Marche, models_etat
from datetime import date, timedelta 


class siteTest(TestCase):

    
    def setUp(self):
        
        self.prestataire1 = Prestataire.objects.create(nom="prestaire1")
        self.siteA = Site.objects.create(prestataire=self.prestataire1, nom=u"siteA")
        
        self.charge_insertion = ChargeInsertion.objects.create(nom="nom", prenom="prénom")
        self.charge_insertion.les_sites.add( self.siteA)
        self.charge_insertion.save()
        
        
        self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)


    def test_lc_stats_empty(self):
        self.assertEqual(0,self.siteA.lc_stats()[models_etat.LC_EN_ATTENTE])
        self.assertEqual(0,self.siteA.lc_stats()[models_etat.LC_EN_COURS])
        self.assertEqual(0,self.siteA.lc_stats()[models_etat.LC_CLOTURE])
        
    
    def test_lc_stats_oneLC(self):
        lc = LettreCommande.objects.create( marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.siteA, 
                                            date_debut=date.today()-timedelta(days=1), date_fin=date.today()+timedelta(days=1))
        self.assertEqual(1,self.siteA.lc_stats()[models_etat.LC_EN_ATTENTE])
        self.assertEqual(0,self.siteA.lc_stats()[models_etat.LC_EN_COURS])
        self.assertEqual(0,self.siteA.lc_stats()[models_etat.LC_CLOTURE])
    
    
    def test_lc_stats_EN_COURS(self):
        lc = LettreCommande.objects.create( marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.siteA, 
                                            date_debut=date.today()-timedelta(days=1),\
                                             date_fin=date.today()+timedelta(days=1),\
                                             avancement=models_etat.LC_EN_COURS)
        self.assertEqual(0,self.siteA.lc_stats()[models_etat.LC_EN_ATTENTE])
        self.assertEqual(1,self.siteA.lc_stats()[models_etat.LC_EN_COURS])
        self.assertEqual(0,self.siteA.lc_stats()[models_etat.LC_CLOTURE])
    
    
    def test_lc_stats_CLOTURE(self):
        lc = LettreCommande.objects.create( marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.siteA, 
                                            date_debut=date.today()-timedelta(days=1),\
                                             date_fin=date.today()+timedelta(days=1),\
                                             avancement=models_etat.LC_CLOTURE)
        self.assertEqual(0,self.siteA.lc_stats()[models_etat.LC_EN_ATTENTE])
        self.assertEqual(0,self.siteA.lc_stats()[models_etat.LC_EN_COURS])
        self.assertEqual(1,self.siteA.lc_stats()[models_etat.LC_CLOTURE])
