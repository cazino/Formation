# -*- coding: utf-8 -*-
import pdb
from django.test import TestCase
from administration.models import LettreCommande, Prestataire, Site, ChargeInsertion, Marche, models_etat
from datetime import date, timedelta 


class prestataireTest(TestCase):

    
     
    def setUp(self):
        self.prestataire1 = Prestataire.objects.create(nom="prestaire1")
        self.siteA = Site.objects.create(prestataire=self.prestataire1, nom=u"siteA")
        self.charge_insertion = ChargeInsertion.objects.create(nom="nom", prenom="prénom")
        self.charge_insertion.save()
        self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)

    def test_lc_stats_empty(self):
        presta = Prestataire.objects.create(nom="prestataire")
        self.assertEqual(0,presta.lc_stats()[models_etat.LC_EN_ATTENTE])
        self.assertEqual(0,presta.lc_stats()[models_etat.LC_EN_COURS])
        self.assertEqual(0,presta.lc_stats()[models_etat.LC_CLOTURE])
        
    def test_lc_stats_oneLC(self):
        lc = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site = self.siteA, \
                                            date_debut=date.today()-timedelta(days=1), date_fin=date.today()+timedelta(days=1))
        self.assertEqual(1,self.prestataire1.lc_stats()[models_etat.LC_EN_ATTENTE])
        self.assertEqual(0,self.prestataire1.lc_stats()[models_etat.LC_EN_COURS])
        self.assertEqual(0,self.prestataire1.lc_stats()[models_etat.LC_CLOTURE])
        
    def test_lc_stats_twoLC(self):
        lc = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site = self.siteA, \
                                            date_debut=date.today()-timedelta(days=1),\
                                             date_fin=date.today()+timedelta(days=1),\
                                             avancement=models_etat.LC_EN_COURS)
        self.assertEqual(0,self.prestataire1.lc_stats()[models_etat.LC_EN_ATTENTE])
        self.assertEqual(1,self.prestataire1.lc_stats()[models_etat.LC_EN_COURS])
        self.assertEqual(0,self.prestataire1.lc_stats()[models_etat.LC_CLOTURE])
        
    def test_lc_stats_threeLC(self):
        lc = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site = self.siteA, \
                                            date_debut=date.today()-timedelta(days=1),\
                                             date_fin=date.today()+timedelta(days=1),\
                                             avancement=models_etat.LC_CLOTURE)
        self.assertEqual(0,self.prestataire1.lc_stats()[models_etat.LC_EN_ATTENTE])
        self.assertEqual(0,self.prestataire1.lc_stats()[models_etat.LC_EN_COURS])
        self.assertEqual(1,self.prestataire1.lc_stats()[models_etat.LC_CLOTURE])
        
        
        
class LinkWithLcTest(TestCase):

    def setUp(self):
        self.prestataire1 = Prestataire.objects.create(nom=u"prestaire1")
        self.siteA = Site.objects.create(prestataire=self.prestataire1, nom=u"siteA")
        self.charge_insertion = ChargeInsertion.objects.create(nom="nom", prenom="prénom")
        self.charge_insertion.save()
        self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)
        self.lc = lc = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site = self.siteA, \
                                            date_debut=date.today()-timedelta(days=1),\
                                             date_fin=date.today()+timedelta(days=1),\
                                             avancement=models_etat.LC_CLOTURE)
    def test_presta(self):
        self.assertEqual(unicode(self.prestataire1), self.lc.prestataire)
        
    def test_presta2(self):
        self.prestataire2 = Prestataire.objects.create(nom=u"prestaire2")
        self.siteB = Site.objects.create(prestataire=self.prestataire2, nom=u"siteB")
        self.lc.site = self.siteB
        self.lc.save()
        self.assertEqual(unicode(self.prestataire2), self.lc.prestataire) 

class SaveTest(TestCase):

    def setUp(self):
        self.prestataire1 = Prestataire.objects.create(nom=u"prestaire1")
        self.siteA = Site.objects.create(prestataire=self.prestataire1, nom=u"siteA")
        self.charge_insertion = ChargeInsertion.objects.create(nom="nom", prenom="prénom")
        self.charge_insertion.save()
        self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site = self.siteA, \
                                            date_debut=date.today()-timedelta(days=1),\
                                             date_fin=date.today()+timedelta(days=1),\
                                             avancement=models_etat.LC_CLOTURE)
        self.lc.prestataire = 'aa'
        self.lc.save() 
        
    def test_presta(self):
        self.assertEqual('prestaire1', self.lc.prestataire)


class ChangePrestaTest(TestCase):

    def setUp(self):
        self.prestataire1 = Prestataire.objects.create(nom=u"prestaire1")
        self.siteA = Site.objects.create(prestataire=self.prestataire1, nom=u"siteA")
        self.charge_insertion = ChargeInsertion.objects.create(nom="nom", prenom="prénom")
        self.charge_insertion.save()
        self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site = self.siteA, \
                                            date_debut=date.today()-timedelta(days=1),\
                                             date_fin=date.today()+timedelta(days=1),\
                                             avancement=models_etat.LC_CLOTURE)
        pdb.set_trace()
        self.prestataire1.nom = 'aa'
        self.prestataire1.save() 
        
    def test_presta(self):
        self.assertEqual('aa', self.lc.prestataire)

        

    