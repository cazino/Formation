from django.test import TestCase
from greta.administration.models import Marche, Prestataire, Site, ChargeInsertion, LettreCommande, Rdv, models_etat
from greta.administration.pdf import bilanPdf
from datetime import date


class emptyRdvTest(TestCase):

    def setUp(self):
        self.marche = Marche.objects.create(polemploi_id='abc', montant_unitaire=1438, portage=0.2)
        self.prestaire = Prestataire.objects.create(nom='prestataire')
        self.site = Site.objects.create(prestataire=self.prestaire, nom="Site")
        self.chargeinsertion = ChargeInsertion.objects.create(nom='Lambert', prenom='Gerard')
        self.lc = LettreCommande.objects.create(marche=self.marche,
                                                charge_insertion=self.chargeinsertion,
                                                site=self.site,
                                                numero_lc='azerty',
                                                date_debut=date(year=2008, month=03, day=12),
                                                date_fin=date(year=2008, month=06, day=20),
                                                civilite=1,
                                                nom='Doe',
                                                prenom='John',
                                                polemploi_id='qsdfg',
                                                ale_prescriptrice='Paris',
                                                conseiller_ploleemploi='Personne',
                                                avancement=models_etat.LC_EN_COURS)
        self.rdv = Rdv.objects.create(lettre_commande=self.lc, present=True, dateheure=date(year=2008, month=03, day=12))
        self.rdvView = bilanPdf.rdvView(self.rdv)
        
        
    def test_persoEvenDate(self):
        self.assertEqual('', self.rdvView._persoEvenDate(number=1))
        
    def test_persoEvenInsti(self):
        self.assertEqual('', self.rdvView._persoEvenInsti(number=1))
        
    def test_persoEvenAction(self):
        self.assertEqual('', self.rdvView._persoEvenAction(number=1))
        
    def test_persoEvenResults(self):
        self.assertEqual('', self.rdvView._persoEvenResults(number=1))
        
    def test_emptyViewEven1(self):
        self.assertEqual([], self.rdvView._persoEven(1))
        
    def test_emptyViewAllEvents(self):
        self.assertEqual([], self.rdvView.persoAllEvents())
     
     
class nonEmptyRdvTest(TestCase):

    def setUp(self):
        self.marche = Marche.objects.create(polemploi_id='abc', montant_unitaire=1438, portage=0.2)
        self.prestaire = Prestataire.objects.create(nom='prestataire')
        self.site = Site.objects.create(prestataire=self.prestaire, nom="Site")
        self.chargeinsertion = ChargeInsertion.objects.create(nom='Lambert', prenom='Gerard')
        self.lc = LettreCommande.objects.create(marche=self.marche,
                                                charge_insertion=self.chargeinsertion,
                                                site=self.site,
                                                numero_lc='azerty',
                                                date_debut=date(year=2008, month=03, day=12),
                                                date_fin=date(year=2008, month=06, day=20),
                                                civilite=1,
                                                nom='Doe',
                                                prenom='John',
                                                polemploi_id='qsdfg',
                                                ale_prescriptrice='Paris',
                                                conseiller_ploleemploi='Personne',
                                                avancement=models_etat.LC_EN_COURS)
        
        self.date1 = 'Janvier 2007'
        self.rdv = Rdv.objects.create(lettre_commande=self.lc, present=True, dateheure=date(year=2008, month=03, day=12),accsoc_date1=self.date1)
        self.rdvView = bilanPdf.rdvView(self.rdv)
        
        
    def test_persoEvenDate(self):
        self.assertEqual(self.date1, self.rdvView._persoEvenDate(number=1))
        
    def test_persoEvenInsti(self):
        self.assertEqual('', self.rdvView._persoEvenInsti(number=1))
        
    def test_persoEvenAction(self):
        self.assertEqual('', self.rdvView._persoEvenAction(number=1))
        
    def test_persoEvenResults(self):
        self.assertEqual('', self.rdvView._persoEvenResults(number=1))
        
    def test_emptyView(self):
        self.assertEqual([self.date1, '', '', ''], self.rdvView._persoEven(1))

    def test_emptyViewAllEvents(self):
        self.assertEqual([[self.date1, '', '', '']], self.rdvView.persoAllEvents())
    


        
        
        
        
        
        