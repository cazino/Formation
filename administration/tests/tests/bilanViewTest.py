from django.test import TestCase
from greta.administration.models import Marche, Prestataire, Site, ChargeInsertion, LettreCommande, Rdv, models_etat
from greta.administration.pdf import bilanPdf   
import datetime

class persoAllEvents1Test(TestCase):

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
        
        self.date1 = 'Janvier 2007'
        self.rdv = Rdv.objects.create(lettre_commande=self.lc, present=True, dateheure=datetime.date(year=2008, month=03, day=12), accsoc_date1=self.date1)
        self.bilanView = bilanPdf.bilanView(self.lc)
        
        
    def test_oneRdv(self):
        self.assertEqual([['Janvier 2007', '', '', '']], self.bilanView.persoAllEvents())
        
        
class persoAllEvents2Test(TestCase):

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
        
        self.date1 = 'Janvier 2007'
        rdv = Rdv.objects.create(lettre_commande=self.lc, present=True, dateheure=datetime.date(year=2008, month=06, day=20), accsoc_date1=self.date1)
    
        
        self.result3 = u"qfdzefzefzefz"
        rdv = Rdv.objects.create(lettre_commande=self.lc, present=True, dateheure=datetime.date(year=2008, month=06, day=25), accsoc_results3=self.result3)
        
        self.bilanView = bilanPdf.bilanView(self.lc)
        
        
    def test_twoRdv(self):
        self.assertEqual([[self.date1, '', '', ''], ['', '', '', self.result3]], self.bilanView.persoAllEvents())
        
        
class persoAllEvents3Test(TestCase):

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
        
        
        self.bilanView = bilanPdf.bilanView(self.lc)
        
        
    def test_noRdv(self):
        self.assertEqual([], self.bilanView.persoAllEvents())
        
        



