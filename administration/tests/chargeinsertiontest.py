# -*- coding: utf-8 -*-
from prestationtest import prestationTest
from administration.models import LettreCommande, ouvertureRdv, Prestataire, Site, ChargeInsertion, models_etat
from datetime import date, datetime, timedelta

class chargeInsertionTest(prestationTest):
    
    def test_LcActif0(self):
        lc1 = LettreCommande.objects.create(site=self.site,\
                                                marche=self.marche,\
                                                  charge_insertion=self.charge_insertion,\
                                                  date_debut=date.today(),\
                                                  date_fin=date.today())
        self.assertEqual(0, self.charge_insertion.lc_actif())
        
    def test_LcActif1(self):
        lc1 = LettreCommande.objects.create(site=self.site,\
                                                marche=self.marche,\
                                                  charge_insertion=self.charge_insertion,\
                                                  date_debut=date.today(),\
                                                  date_fin=date.today())
        lc1.changeAvancement(models_etat.LC_EN_COURS)
        self.assertEqual(1, self.charge_insertion.lc_actif())
        
    def testLcAttente(self):
        lc1 = LettreCommande.objects.create(site=self.site,\
                                                marche=self.marche,\
                                                  charge_insertion=self.charge_insertion,\
                                                  date_debut=date.today(),\
                                                  date_fin=date.today())
        self.assertEqual(1, self.charge_insertion.lc_attente())
        
    def testLcAttente2(self):
        lc1 = LettreCommande.objects.create(site=self.site,\
                                                marche=self.marche,\
                                                  charge_insertion=self.charge_insertion,\
                                                  date_debut=date.today(),\
                                                  date_fin=date.today())
        lc1.changeAvancement(models_etat.LC_EN_COURS)
        self.assertEqual(0, self.charge_insertion.lc_attente())
        
        
    def testtutu(self):
        prestataire = Prestataire.objects.create(nom='prestataire')
        site = Site.objects.create(nom='prestataire-site', prestataire=self.prestataire)
        charge_insertion = ChargeInsertion.objects.create(nom="nom", prenom="prénom")
        charge_insertion.les_sites.add(site)          
        self.assertEqual(site, charge_insertion.les_sites.iterator().next())
        
    def test_LesSites(self):
        prestataire = Prestataire.objects.create(nom='prestataire')
        site = Site.objects.create(nom='prestataire-site', prestataire=self.prestataire)
              
        charge_insertion = ChargeInsertion.objects.create(nom="nom", prenom="prénom")
        charge_insertion.les_sites.add(site)
              
        #self.assertEqual('prestataire-site', charge_insertion.les_sites.iterator().next().nom)
        self.assertEqual('prestataire-site', charge_insertion.lesSites())
    
                
"""



class chargeInsertionTest(prestationTest):
              
    
        
                
    
        
    
    
        
        
        
    
    
    

"""