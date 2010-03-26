from django.test import TestCase
from greta.administration.models import Marche, Prestataire, Site, ChargeInsertion, LettreCommande, models_etat
from greta.administration.csv import csvResponse 
import datetime


class lcEncoursTest(TestCase):

    def setUp(self):
        self.marche = Marche.objects.create(polemploi_id='abc', montant_unitaire=1438, portage=0.2)
        self.prestaire = Prestataire.objects.create(nom='prestataire')
        self.site = Site.objects.create(prestataire=self.prestaire, nom="Site")
        self.chargeinsertion = ChargeInsertion.objects.create(nom='Lambert', prenom='Gerard')
        self.lc = LettreCommande.objects.create(marche=self.marche,
                                                charge_insertion=self.chargeinsertion,
                                                site=self.site,
                                                numero_lc='azerty',
                                                date_debut=datetime.date(year=2008, month=03, day=12),
                                                date_fin=datetime.date(year=2008, month=06, day=20),
                                                civilite=1,
                                                nom='Doe',
                                                prenom='John',
                                                polemploi_id='qsdfg',
                                                ale_prescriptrice='Paris',
                                                conseiller_ploleemploi='Personne',
                                                avancement=models_etat.LC_EN_COURS)
        
        self.refDay = datetime.date(year=2008, month=05, day=12)
        self.lc_csvView = csvResponse.csvView(self.lc, self.refDay)
        self.lc_csvDict = self.lc_csvView.csvDict() 
        
    def test_numlc(self):
        self.assertEqual('azerty', self.lc_csvDict['NUM LC'][1])
        
    def test_numconvention(self):
        self.assertEqual('abc', self.lc_csvDict['NUM CONVENTION'][1])
        
    def test_dateentree(self):
        self.assertEqual('12/03/2008', self.lc_csvDict['DATE ENTREE'][1])
        
    def test_datesortie(self):
        self.assertEqual('20/06/2008', self.lc_csvDict['DATE SORTIE'][1])
        
    def test_montant(self):
        self.assertEqual(1438, self.lc_csvDict['MONTANT LC'][1])
        
    def test_civilite(self):
        self.assertEqual(1, self.lc_csvDict['CIVILITE'][1])
        
    def test_nom(self):
        self.assertEqual('Doe', self.lc_csvDict['NOM'][1])
        
    def test_prenom(self):
        self.assertEqual('John', self.lc_csvDict['PRENOM'][1])
        
    def test_identifiant(self):
        self.assertEqual('qsdfg', self.lc_csvDict['IDENTIFIANT'][1])
        
    def test_ale(self):
        self.assertEqual('Paris', self.lc_csvDict['ALE'][1])
        
    def test_prestataire(self):
        self.assertEqual('prestataire', self.lc_csvDict['PRESTATAIRE'][1])
    
    def test_entreePresta(self):
        self.assertEqual(1, self.lc_csvDict['ENTREE EN PRESTATION'][1])
    
    def test_referent(self):
        self.assertEqual('Lambert', self.lc_csvDict['REFERENT'][1])


    
    def test_prestaEcoule(self):
        self.assertEqual(0, self.lc_csvDict['2007'][1])
        self.assertEqual(0, self.lc_csvDict['JANVIER'][1])
        self.assertEqual(0, self.lc_csvDict['FEVRIER'][1])
        self.assertEqual(20, self.lc_csvDict['MARS'][1])
        self.assertEqual(30, self.lc_csvDict['AVRIL'][1])
        self.assertEqual(12, self.lc_csvDict['MAI'][1])
        self.assertEqual(0, self.lc_csvDict['JUIN'][1])
        self.assertEqual(0, self.lc_csvDict['JUILLET'][1])
        self.assertEqual(0, self.lc_csvDict['AOUT'][1])
        self.assertEqual(0, self.lc_csvDict['SEPTEMBRE'][1])
        self.assertEqual(0, self.lc_csvDict['OCTOBRE'][1])
        self.assertEqual(0, self.lc_csvDict['NOVEMBRE'][1])
        self.assertEqual(0, self.lc_csvDict['DECEMBRE'][1])
    
    def test_nbjours(self):
        self.assertEqual(62, self.lc_csvDict['NB DE JOURS'][1])
        
    def test_datesortie(self):
        self.assertEqual(None, self.lc_csvDict['DATE SORTIE REELLE'][1])
        
    def test_montantfacturable(self):
        self.assertAlmostEqual(first=495.31, second=self.lc_csvDict['MONTANT FACTURABLE'][1], places=2) 
       
       
class privateMethodTest(TestCase):
     
    def setUp(self):
        self.marche = Marche.objects.create(polemploi_id='abc', montant_unitaire=1438, portage=0.2)
        self.prestaire = Prestataire.objects.create(nom='prestataire')
        self.site = Site.objects.create(prestataire=self.prestaire, nom="Site")
        self.chargeinsertion = ChargeInsertion.objects.create(nom='Lambert', prenom='Gerard')
        self.lc = LettreCommande.objects.create(marche=self.marche,
                                                charge_insertion=self.chargeinsertion,
                                                site=self.site,
                                                numero_lc='azerty',
                                                date_debut=datetime.date(day=12, month=11, year=2008),
                                                date_fin=datetime.date(day=20,  month=03, year=2009),
                                                civilite=1,
                                                nom='Doe',
                                                prenom='John',
                                                polemploi_id='qsdfg',
                                                ale_prescriptrice='Paris',
                                                conseiller_ploleemploi='Personne',
                                                avancement=models_etat.LC_EN_COURS)
        self.refDay = datetime.date(year=2009, month=02, day=12)
        self.lc_csvView = csvResponse.csvView(self.lc, self.refDay)
     
    def test_lastDay(self):
        self.assertEqual(self.refDay, self.lc_csvView.lastDay)
        
    def test_daysUsedYearbefore(self):
        self.assertEqual(50, self.lc_csvView.daysUsedYearbefore())       
        
    def test_daysUsedMonth(self): 
        self.assertEqual(31, self.lc_csvView.daysUsedMonth(month=1))
        self.assertEqual(12, self.lc_csvView.daysUsedMonth(month=2))
        self.assertEqual(0, self.lc_csvView.daysUsedMonth(month=3))
        
                
       