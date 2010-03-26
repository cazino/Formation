# -*- coding: utf-8 -*-
import pdb
import random
from datetime import datetime, date, timedelta
from django.test import TestCase
from greta.administration.models import Prestataire, Site, Marche, ChargeInsertion, LettreCommande, ouvertureRdv, Cloture, Frein, models_etat
from greta.administration.stat.calcul import StatResult, FreinResult, LCStatCalc, SiteCalc, LCFreinResult, LCFreinCalc


class StatResultTest(TestCase):

    def setUp(self):
       result = StatResult() 
        
    def test_init(self):
        pass

    def test_empty_comparaison(self):
        result1 = StatResult()
        result2 = StatResult()
        self.assert_(result1 == result2)
        
    def test_false_comparaison(self):
        result1 = StatResult()
        result2 = StatResult()
        result2.premier_rdv_absent = 1
        self.assertFalse(result1 == result2)
        
    def test_empty_addition(self):
        result1 = StatResult()
        result2 = StatResult()
        self.assertEqual(StatResult(), result1 + result2)
        
    def test_addition_1(self):
        result1 = StatResult()
        result1.premier_rdv_absent = 5
        result2 = StatResult()
        result2.premier_rdv_absent = 6
        expected_result = StatResult()
        expected_result.premier_rdv_absent = 11
        self.assertEqual(expected_result, result1 + result2)
        
    def test_addition_2(self):
        result1 = StatResult()
        result1.premier_rdv_absent = 5
        result1.abandon_5 = 2
        
        result2 = StatResult()
        result2.premier_rdv_absent = 6
        
        expected_result = StatResult()
        expected_result.premier_rdv_absent = 11
        expected_result.abandon_5 = 2
        self.assertEqual(expected_result, result1 + result2)
        
    
class LCStatCalcTest(TestCase):
    
    def setUp(self):
        self.prestataire = Prestataire.objects.create(nom=u"prestaire")
        self.site = Site.objects.create(prestataire=self.prestataire, nom=u"site")
        self.charge_insertion = ChargeInsertion.objects.create(nom=u"nom", prenom=u"prénom")
        self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)
        self.datetime_ouverture = datetime.today()-timedelta(days=50)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_COURS)
    def tearDown(self):
        self.prestataire.delete()
        self.site.delete()
        self.charge_insertion.delete()
        self.marche.delete()
        self.lc.delete()
        
    def test_init(self):
        self.assert_(LCStatCalc(None))
            
    def test_rdv_absent(self):
        self.ouverture_rdv = ouvertureRdv(lettre_commande=self.lc, 
                                          dateheure=self.datetime_ouverture,
                                          statut=ouvertureRdv.ABSENT)
        self.ouverture_rdv.save()
        expected_result = StatResult()
        expected_result.premier_rdv_absent = 1
        produced_result = LCStatCalc(self.lc).calculate()
        self.assertEqual(expected_result, produced_result)
        
    def test_rdv_report(self):
        self.ouverture_rdv = ouvertureRdv(lettre_commande=self.lc, 
                                          dateheure=self.datetime_ouverture,
                                          statut=ouvertureRdv.REPORT)
        self.ouverture_rdv.save()
        expected_result = StatResult()
        expected_result.premier_rdv_report = 1
        produced_result = LCStatCalc(self.lc).calculate()
        self.assertEqual(expected_result, produced_result)
        
    def test_abandon_un_mois(self):
        self.cloture = Cloture(lettre_commande=self.lc,
                               terme=False, 
                               date_abandon=self.datetime_ouverture.date()+timedelta(days=10))
        self.cloture.save()
        expected_result = StatResult()
        expected_result.abandon_1 = 1
        produced_result = LCStatCalc(self.lc).calculate()
        self.assertEqual(expected_result, produced_result)
        
    def test_abandon_deux_mois(self):
        self.cloture = Cloture(lettre_commande=self.lc,
                               terme=False, 
                               date_abandon=self.datetime_ouverture.date()+timedelta(days=40))
        self.cloture.save()
        expected_result = StatResult()
        expected_result.abandon_2 = 1
        produced_result = LCStatCalc(self.lc).calculate()
        self.assertEqual(expected_result, produced_result)

    def test_abandon_trois_mois(self):
        self.cloture = Cloture(lettre_commande=self.lc,
                               terme=False, 
                               date_abandon=self.datetime_ouverture.date()+timedelta(days=70))
        self.cloture.save()
        expected_result = StatResult()
        expected_result.abandon_3 = 1
        produced_result = LCStatCalc(self.lc).calculate()
        self.assertEqual(expected_result, produced_result)
        
    def test_abandon_quatre_mois(self):
        self.cloture = Cloture(lettre_commande=self.lc,
                               terme=False, 
                               date_abandon=self.datetime_ouverture.date()+timedelta(days=100))
        self.cloture.save()
        expected_result = StatResult()
        expected_result.abandon_4 = 1
        produced_result = LCStatCalc(self.lc).calculate()
        self.assertEqual(expected_result, produced_result)   
        
    def test_abandon_cinq_mois(self):
        self.cloture = Cloture(lettre_commande=self.lc,
                               terme=False, 
                               date_abandon=self.datetime_ouverture.date()+timedelta(days=130))
        self.cloture.save()
        expected_result = StatResult()
        expected_result.abandon_5 = 1
        produced_result = LCStatCalc(self.lc).calculate()
        self.assertEqual(expected_result, produced_result)
        
    def test_abandon_six_mois(self):
        self.cloture = Cloture(lettre_commande=self.lc,
                               terme=False, 
                               date_abandon=self.datetime_ouverture.date()+timedelta(days=160))
        self.cloture.save()
        expected_result = StatResult()
        expected_result.abandon_6 = 1
        produced_result = LCStatCalc(self.lc).calculate()
        self.assertEqual(expected_result, produced_result)
        
            

class FreinResultTest(TestCase):
    
    def setUp(self): 
        self.frein_number = random.randint(0,3)
        self.frein = Frein.nom_freins[self.frein_number]
        self.valeurs =  Frein.valeurs_freins[self.frein_number]
        
    def test_init(self):
        self.assert_(FreinResult(self.frein, self.valeurs))
        
    def test_add(self):
         expected_result = FreinResult(self.frein, self.valeurs)
         expected_result.all_frein[self.valeurs[1]] += 1
         produced_result = FreinResult(self.frein, self.valeurs)
         produced_result.add(self.valeurs[1])
         self.assertEqual(expected_result, produced_result)
         
    def test_add_first(self):
         expected_result = FreinResult(self.frein, self.valeurs)
         expected_result.all_frein[self.valeurs[1]] += 1
         expected_result.first_frein[self.valeurs[1]] += 1
         produced_result = FreinResult(self.frein, self.valeurs)
         produced_result.add_first(self.valeurs[1])
         self.assertEqual(expected_result, produced_result)
         
    def test_empty_equal(self):
        self.assertEqual(FreinResult(self.frein, self.valeurs), FreinResult(self.frein, self.valeurs))
        
    def test_empty_addition(self):
        expected_result = FreinResult(self.frein, self.valeurs)
        produced_result = FreinResult(self.frein, self.valeurs) + FreinResult(self.frein, self.valeurs)
        self.assertEqual(expected_result, produced_result)
        
    def test_not_empty_addition(self):
        expected_result = FreinResult(self.frein, self.valeurs)
        expected_result.first_frein[self.valeurs[1]] += 1
        tmp_result = FreinResult(self.frein, self.valeurs)
        tmp_result.first_frein[self.valeurs[1]] += 1
        produced_result = FreinResult(self.frein, self.valeurs) + tmp_result
        self.assertEqual(expected_result, produced_result)
        
class LCFreinResultTest(TestCase):
    
    def test_init(self):
        self.assert_(LCFreinResult())
        
    def test_add(self):
         frein_categorie = Frein.PRO_INTIT
         frein_valeur = Frein.PRO_ETU
         expected_result = LCFreinResult()
         expected_result.frein_result_dic[frein_categorie].all_frein[frein_valeur] += 1
         produced_result = LCFreinResult()
         produced_result.add(frein_categorie, frein_valeur)
         self.assertEqual(expected_result, produced_result)

    def test_add_first(self):
         frein_categorie = Frein.PRO_INTIT
         frein_valeur = Frein.PRO_ETU
         expected_result = LCFreinResult()
         expected_result.frein_result_dic[frein_categorie].all_frein[frein_valeur] += 1
         expected_result.frein_result_dic[frein_categorie].first_frein[frein_valeur] += 1
         produced_result = LCFreinResult()
         produced_result.add_first(frein_categorie, frein_valeur)
         self.assertEqual(expected_result, produced_result)

    def test_empty_addition(self):
        self.assertEqual(LCFreinResult(),  LCFreinResult() +  LCFreinResult())
        
    def test_addition(self):
        lc_frein_result_1 = LCFreinResult()
        lc_frein_result_1.add(Frein.PRO_INTIT, Frein.PRO_ETU)
        lc_frein_result_2 = LCFreinResult()
        lc_frein_result_2.add(Frein.PRO_INTIT, Frein.PRO_ETU)
        expected_result = LCFreinResult()
        expected_result.add(Frein.PRO_INTIT, Frein.PRO_ETU)
        expected_result.add(Frein.PRO_INTIT, Frein.PRO_ETU)
        self.assertEqual(expected_result,  lc_frein_result_1 + lc_frein_result_2)


class LCFreinCalcTest(TestCase):
    
    def setUp(self):
        self.prestataire = Prestataire.objects.create(nom=u"prestaire")
        self.site = Site.objects.create(prestataire=self.prestataire, nom=u"site")
        self.charge_insertion = ChargeInsertion.objects.create(nom=u"nom", prenom=u"prénom")
        self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)
        self.date_debut = date(day=1, month=2, year=2000)
        self.date_fin = date(day=1, month=2, year=2010)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.date_debut,\
                                                date_fin=self.date_fin,\
                                                avancement=models_etat.LC_EN_ATTENTE)      
    
    def test_empty_lc(self):
        self.assertEqual(LCFreinResult(), LCFreinCalc(self.lc).calculate())
        
    
    def test_complicated(self):
        self.frein = Frein.objects.create(lettre_commande=self.lc,
                                          pro1=Frein.PRO_EXPE,
                                          pro2 = Frein.PRO_PP)
        expected_result = LCFreinResult()
        expected_result.add_first(Frein.PRO_INTIT, Frein.PRO_EXPE)
        expected_result.add(Frein.PRO_INTIT, Frein.PRO_PP)
        self.assertEqual(expected_result , LCFreinCalc(self.lc).calculate())
     
     
class SiteCalcStatTest(TestCase):
    
    def setUp(self):
        self.prestataire = Prestataire.objects.create(nom=u"prestaire")
        self.site = Site.objects.create(prestataire=self.prestataire, nom=u"site")
        self.charge_insertion = ChargeInsertion.objects.create(nom=u"nom", prenom=u"prénom")
        self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)
        self.date_debut = date(day=1, month=2, year=2000)
        self.date_fin = date(day=1, month=2, year=2010)  
        
    def tearDown(self):
        self.prestataire.delete()
        self.site.delete()
        self.charge_insertion.delete()
        self.marche.delete()
        
    def test_empty_site(self):
        self.assertEqual(StatResult(), SiteCalc(self.site, self.date_debut, self.date_fin).calculate()[0]) 
        
    def test_one_lc_site(self):
        self.datetime_ouverture = datetime.today()-timedelta(days=50)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_COURS)    
        self.ouverture_rdv = ouvertureRdv(lettre_commande=self.lc, 
                                          dateheure=self.datetime_ouverture,
                                          statut=ouvertureRdv.ABSENT)
        self.ouverture_rdv.save()
        expected_result = StatResult()
        expected_result.premier_rdv_absent = 1
        self.assertEqual(expected_result, SiteCalc(self.site, self.date_debut, self.date_fin).calculate()[0])
        self.lc.delete()
        self.ouverture_rdv.delete()
        
    def test_two_lc_site(self):
        self.datetime_ouverture = datetime.today()-timedelta(days=50)
        self.lc1 = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_COURS)    
        self.ouverture_rdv1 = ouvertureRdv(lettre_commande=self.lc1, 
                                          dateheure=self.datetime_ouverture,
                                          statut=ouvertureRdv.ABSENT)
        self.ouverture_rdv1.save()
        self.lc2 = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_COURS)    
        self.ouverture_rdv2 = ouvertureRdv(lettre_commande=self.lc2, 
                                          dateheure=self.datetime_ouverture,
                                          statut=ouvertureRdv.ABSENT)
        self.ouverture_rdv2.save()
        
        expected_result = StatResult()
        expected_result.premier_rdv_absent = 2
        self.assertEqual(expected_result, SiteCalc(self.site, self.date_debut, self.date_fin).calculate()[0])
        self.lc1.delete()
        self.ouverture_rdv1.delete()
        self.lc2.delete()
        self.ouverture_rdv2.delete()
        
    def test_empty_result_because_inadequate_period(self):
        self.datetime_ouverture = datetime.today()-timedelta(days=50)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_COURS)    
        self.ouverture_rdv = ouvertureRdv(lettre_commande=self.lc, 
                                          dateheure=self.datetime_ouverture,
                                          statut=ouvertureRdv.ABSENT)
        self.ouverture_rdv.save()
        old_date = date(day=1, month=1, year=199)
        self.assertEqual(StatResult(), SiteCalc(self.site, old_date, old_date).calculate()[0])
        self.lc.delete()
        self.ouverture_rdv.delete()
        
    def test_empty_result_because_lc_en_attente(self):
        self.datetime_ouverture = datetime.today()-timedelta(days=50)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_ATTENTE)    
        
        old_date = self.datetime_ouverture.date()
        self.assertEqual(StatResult(), SiteCalc(self.site, old_date, old_date).calculate()[0])
        self.lc.delete()
        

        
class SiteCalcFreinTest(TestCase):
    
    def setUp(self):
        self.prestataire = Prestataire.objects.create(nom=u"prestaire")
        self.site = Site.objects.create(prestataire=self.prestataire, nom=u"site")
        self.charge_insertion = ChargeInsertion.objects.create(nom=u"nom", prenom=u"prénom")
        self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)
        self.date_debut = date(day=1, month=2, year=2000)
        self.date_fin = date(day=1, month=2, year=2010)  
        
    def tearDown(self):
        self.prestataire.delete()
        self.site.delete()
        self.charge_insertion.delete()
        self.marche.delete()
        
    def test_empty_site(self):
        self.assertEqual(LCFreinResult(), SiteCalc(self.site, self.date_debut, self.date_fin).calculate()[1]) 
    
    def test_one_lc_site(self):
        self.datetime_ouverture = datetime.today()-timedelta(days=50)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_COURS)    
        self.frein = Frein.objects.create(lettre_commande=self.lc, pro1=Frein.PRO_PP)
        expected_result = LCFreinResult()
        expected_result.add_first(Frein.PRO_INTIT, Frein.PRO_PP)
        self.assertEqual(expected_result, SiteCalc(self.site, self.date_debut, self.date_fin).calculate()[1])
        self.lc.delete()
        self.frein.delete()
        
    def test_two_lc_site(self):
        self.datetime_ouverture = datetime.today()-timedelta(days=50)
        self.lc1 = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_COURS)    
        self.frein1 = Frein.objects.create(lettre_commande=self.lc1, pro1=Frein.PRO_PP)
        self.lc2 = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_COURS)    
        self.frein2 = Frein.objects.create(lettre_commande=self.lc2, pro1=Frein.PRO_PP)
        
        expected_result = LCFreinResult()
        expected_result.add_first(Frein.PRO_INTIT, Frein.PRO_PP)
        expected_result.add_first(Frein.PRO_INTIT, Frein.PRO_PP)
        self.assertEqual(expected_result, SiteCalc(self.site, self.date_debut, self.date_fin).calculate()[1])
        self.lc1.delete()
        self.frein1.delete()
        self.lc2.delete()
        self.frein2.delete()
    
        
    def test_empty_result_because_inadequate_period(self):
        self.datetime_ouverture = datetime.today()-timedelta(days=50)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_COURS)    
        
        old_date = date(day=1, month=1, year=199)
        self.assertEqual(LCFreinResult(), SiteCalc(self.site, old_date, old_date).calculate()[1])
        self.lc.delete()
        
    
       
    def test_empty_result_because_lc_en_attente(self):
        self.datetime_ouverture = datetime.today()-timedelta(days=50)
        self.lc = LettreCommande.objects.create(marche=self.marche,\
                                                charge_insertion=self.charge_insertion,\
                                                site = self.site, \
                                                date_debut=self.datetime_ouverture.date(),\
                                                date_fin=date.today()+timedelta(days=100),\
                                                avancement=models_etat.LC_EN_ATTENTE)    
        
        old_date = self.datetime_ouverture.date()
        self.assertEqual(LCFreinResult(), SiteCalc(self.site, old_date, old_date).calculate()[1])
        self.lc.delete()
     

    