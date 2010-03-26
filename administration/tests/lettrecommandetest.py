# -*- coding: utf-8 -*-
from django.test import TestCase
from prestationtest import prestationTest
from administration.models import LettreCommande, ouvertureRdv, Rdv, Cloture, models_etat
from datetime import date, datetime, timedelta


class lettreCommandeTest(prestationTest):

    

    def test_PrimaryKey(self):
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=date.today(),\
                                            date_fin=date.today())
        key = lc1.pk
        lc1.save()
        self.assertEqual(key,lc1.pk)

    def test_etat_default(self):
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=date.today(),\
                                            date_fin=date.today())
        self.assertEqual(models_etat.LC_EN_ATTENTE, lc1.avancement)
        
        
    def testLastRdv(self):
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=date.today(),\
                                            date_fin=date.today())
        self.assertEqual(None, lc1.lastRdv())
        openRdv = ouvertureRdv.objects.create(lettre_commande=lc1, dateheure=datetime.today(), statut=ouvertureRdv.PRESENT_C)
        self.assertEqual(openRdv, lc1.lastRdv())
        normalRdv = Rdv.objects.create(lettre_commande=lc1, dateheure=datetime.today())
        self.assertEqual(normalRdv, lc1.lastRdv())
        
   
    def testLastRdvDate(self):
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=date.today(),\
                                            date_fin=date.today())
        self.assertEqual(None, lc1.lastRdvDate())
        openRdv = ouvertureRdv.objects.create(lettre_commande=lc1, dateheure=datetime.today(), statut=ouvertureRdv.PRESENT_C)
        self.assertEqual(date.today(), lc1.lastRdvDate())
        tomorow = datetime.today()+timedelta(days=1)
        normalRdv = Rdv.objects.create(lettre_commande=lc1, dateheure=tomorow)
        self.assertEqual(tomorow.date(), lc1.lastRdvDate())
        
    
        
    def test_lastDayPresta1(self):
        debut = date(year=2006, month=03, day=04)
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=debut,\
                                            date_fin=debut+timedelta(days=100))
        self.assertEqual(None, lc1.lastDayPresta())
        
    def test_lastDayPresta2(self):
        debut = date(year=2006, month=03, day=04)
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=debut,\
                                            date_fin=debut+timedelta(days=100), avancement=models_etat.LC_CLOTURE)
        self.assertEqual(debut+timedelta(days=100), lc1.lastDayPresta())
        
    def test_lastDayPresta3(self):
        debut = date(year=2006, month=03, day=04)
        fin = date(year=2006, month=05, day=04)
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=debut,\
                                            date_fin=debut+timedelta(days=100), avancement=models_etat.LC_EN_COURS)
        cloture = Cloture.objects.create(lettre_commande=lc1, terme=False, date_abandon=fin)
        self.assertEqual(fin, lc1.lastDayPresta())
        
    def test_lastDayPresta4(self):
        debut = date(year=2006, month=03, day=04)
        fin = date(day=05, month=05, year=2006)
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=debut,\
                                            date_fin=debut+timedelta(days=99), avancement=models_etat.LC_EN_COURS)
        cloture = Cloture.objects.create(lettre_commande=lc1, terme=False, date_abandon=fin)
        self.assertEqual(fin, lc1.lastDayPresta())
    
    
class notify_prestataire_save_Test(TestCase):
    
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
        self.prestataire1.nom = u"Prout"
        self.lc.notify_prestataire_save(self.prestataire1)
        
        def test_presta(self):
            self.assertEqual(unicode(self.prestataire1), self.lc.prestataire)
   
    
        
