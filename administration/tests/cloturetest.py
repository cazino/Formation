# -*- coding: utf-8 -*-
from prestationtest import prestationTest
from administration.models import LettreCommande, Cloture, models_etat
from datetime import date


class clotureTest(prestationTest):
    
    def testCloture(self):
        lc = LettreCommande.objects.create(site=self.site, marche=self.marche,\
                                           charge_insertion=self.charge_insertion,\
                                           avancement=models_etat.LC_EN_COURS,\
                                           date_debut=date.today(),\
                                           date_fin=date.today())
        cloture = Cloture.objects.create(lettre_commande=lc, terme=True)
        self.assertEqual(models_etat.LC_CLOTURE, lc.avancement)
    
    
    def testClotureDelete(self):
        lc = LettreCommande.objects.create(site=self.site, marche=self.marche,\
                                           charge_insertion=self.charge_insertion,\
                                           avancement=models_etat.LC_CLOTURE,\
                                           date_debut=date.today(),\
                                           date_fin=date.today())
        cloture = Cloture.objects.create(lettre_commande=lc, terme=True)
        cloture.delete()
        self.assertEqual(models_etat.LC_EN_COURS, lc.avancement)
    
    
    def testAbandonInit(self):
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=date.today(),\
                                            date_fin=date.today())
        self.assertEqual(None, lc1.abandon)
        
        
    def testAbandonInit(self):
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=date.today(),\
                                            date_fin=date.today())
        self.assertEqual(False, lc1.abandon)
        
    def testAbandonAband(self):
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=date.today(),\
                                            date_fin=date.today(),
                                            avancement=models_etat.LC_EN_COURS)
        cloture = Cloture.objects.create(lettre_commande=lc1, terme=False)
        self.assertEqual(True, lc1.abandon)

    def test_terme_then_abdandon(self):
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=date.today(),\
                                            date_fin=date.today(),
                                            avancement=models_etat.LC_EN_COURS)
        cloture1 = Cloture.objects.create(lettre_commande=lc1, terme=True)
        cloture1.terme = False
        cloture1.save()
        self.assertEqual(True, lc1.abandon)

