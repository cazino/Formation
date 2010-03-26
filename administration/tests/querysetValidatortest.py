# -*- coding: utf-8 -*-
from django.test import TestCase
from greta.administration.models import LettreCommande, Marche, Prestataire, Site, ChargeInsertion, models_etat
from greta.administration.admin import querySetValidator
import datetime


class masterQuerySetTest(TestCase):
    
    def setUp(self):
        self.marche = Marche.objects.create(polemploi_id='abc', montant_unitaire=1438, portage=0.2)
        self.prestaire = Prestataire.objects.create(nom='prestataire')
        self.site = Site.objects.create(prestataire=self.prestaire, nom="Site")
        self.chargeinsertion = ChargeInsertion.objects.create(nom='Lambert', prenom='Gerard')
        
        
class onePopulated_QuerySetTest(masterQuerySetTest):

    def setUp(self):
        super(onePopulated_QuerySetTest, self).setUp()
        self.lc1 = LettreCommande.objects.create(marche=self.marche,
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
        

    def test_goodqueryset(self):
        result = querySetValidator(LettreCommande.objects.all()).onePopulated() 
        self.assert_(result[0])
        self.assertEqual('', result[1])
        
    def test_toopopulated_queryset(self):
        self.lc2 = LettreCommande.objects.create(marche=self.marche,
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
        result = querySetValidator(LettreCommande.objects.all()).onePopulated() 
        self.assertEqual(False, result[0])
        self.assertEqual(u"Veuillez sélectionner une seule lettre de commande", result[1])
    
        
    def tearDown(self):
        self.lc1 = None 
        self.lc2 = None
        LettreCommande.objects.all().delete()
        
        

class oneNotEnAttente_QuerySetTest(masterQuerySetTest):

    def setUp(self):
        super(oneNotEnAttente_QuerySetTest, self).setUp()
        self.lc1 = LettreCommande.objects.create(marche=self.marche,
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
    
    def testGoodQuerySet(self):
        result = querySetValidator(LettreCommande.objects.all()).oneNotEnAttente() 
        self.assertEqual(True, result[0])
        self.assertEqual('', result[1])
        
    def testTooMuchPopulated_QuerySet(self):
        result = querySetValidator(LettreCommande.objects.all()).oneNotEnAttente()
        self.lc2 = LettreCommande.objects.create(marche=self.marche,
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
        result = querySetValidator(LettreCommande.objects.all()).oneNotEnAttente()  
        self.assertEqual(False, result[0])
        self.assertEqual(u"Veuillez sélectionner une seule lettre de commande", result[1])
        
    def testLcInWrongState_QuerySet(self):
        self.lc1.avancement=models_etat.LC_EN_ATTENTE
        self.lc1.save()
        result = querySetValidator(LettreCommande.objects.all()).oneNotEnAttente()  
        self.assertEqual(False, result[0])
        self.assertEqual(u"La lettre de commande sélectionnée est en attente", result[1])        

    def tearDown(self):
        self.lc1 = None 
        self.lc2 = None
        LettreCommande.objects.all().delete()
        
        
class oneAbandonnee_QuerySetTest(masterQuerySetTest):

    def setUp(self):
        super(oneAbandonnee_QuerySetTest, self).setUp()
        self.lc1 = LettreCommande.objects.create(marche=self.marche,
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
                                                avancement=models_etat.LC_EN_COURS,
                                                abandon=True)
    
    def testGoodQuerySet(self):
        result = querySetValidator(LettreCommande.objects.all()).oneAbandonnee() 
        self.assertEqual(True, result[0])
        self.assertEqual('', result[1])
        
    def testTooMuchPopulated_QuerySet(self):
        result = querySetValidator(LettreCommande.objects.all()).oneNotEnAttente()
        self.lc2 = LettreCommande.objects.create(marche=self.marche,
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
        result = querySetValidator(LettreCommande.objects.all()).oneAbandonnee()  
        self.assertEqual(False, result[0])
        self.assertEqual(u"Veuillez sélectionner une seule lettre de commande", result[1])
        
    def testLcInWrongState_QuerySet(self):
        self.lc1.abandon = False
        self.lc1.save()
        result = querySetValidator(LettreCommande.objects.all()).oneAbandonnee()  
        self.assertEqual(False, result[0])
        self.assertEqual(u"La lettre de commande sélectionnée n'est pas abandonnée", result[1])      
    
    def tearDown(self):
        self.lc1 = None 
        self.lc2 = None
        LettreCommande.objects.all().delete()
        
        
        
        
class oneEntreEnPresta_QuerySetTest(masterQuerySetTest):

    def setUp(self):
        super(oneEntreEnPresta_QuerySetTest, self).setUp()
        self.lc1 = LettreCommande.objects.create(marche=self.marche,
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
    
    def testGoodQuerySet(self):
        result = querySetValidator(LettreCommande.objects.all()).oneEntreEnPresta() 
        self.assertEqual(True, result[0])
        self.assertEqual('', result[1])
        
    
    def testTooMuchPopulated_QuerySet(self):
        result = querySetValidator(LettreCommande.objects.all()).oneNotEnAttente()
        self.lc2 = LettreCommande.objects.create(marche=self.marche,
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
        result = querySetValidator(LettreCommande.objects.all()).oneEntreEnPresta() 
        self.assertEqual(False, result[0])
        self.assertEqual(u"Veuillez sélectionner une seule lettre de commande", result[1])
    
    def testLcInWrongState_QuerySet(self):
        self.lc1.avancement=models_etat.LC_EN_ATTENTE
        self.lc1.save()
        result = querySetValidator(LettreCommande.objects.all()).oneEntreEnPresta()  
        self.assertEqual(False, result[0])
        self.assertEqual(u"Le bénéficiaire n'est pas entré en prestation", result[1])   
    
    def tearDown(self):
        self.lc1 = None 
        self.lc2 = None
        LettreCommande.objects.all().delete()
    

class oneCloture_QuerySetTest(masterQuerySetTest):

    def setUp(self):
        super(oneCloture_QuerySetTest, self).setUp()
        self.lc1 = LettreCommande.objects.create(marche=self.marche,
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
                                                avancement=models_etat.LC_CLOTURE)
    
    def testGoodQuerySet(self):
        result = querySetValidator(LettreCommande.objects.all()).oneCloture() 
        self.assertEqual(True, result[0])
        self.assertEqual('', result[1])
        
    
    def testTooMuchPopulated_QuerySet(self):
        result = querySetValidator(LettreCommande.objects.all()).oneNotEnAttente()
        self.lc2 = LettreCommande.objects.create(marche=self.marche,
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
        result = querySetValidator(LettreCommande.objects.all()).oneCloture() 
        self.assertEqual(False, result[0])
        self.assertEqual(u"Veuillez sélectionner une seule lettre de commande", result[1])
        
    
    def testLcInWrongState_QuerySet(self):
        self.lc1.avancement=models_etat.LC_EN_ATTENTE
        self.lc1.save()
        result = querySetValidator(LettreCommande.objects.all()).oneCloture()  
        self.assertEqual(False, result[0])
        self.assertEqual(u"La lettre de commande n'est pas cloturée", result[1])
       
    
    def tearDown(self):
        self.lc1 = None 
        self.lc2 = None
        LettreCommande.objects.all().delete()
    
