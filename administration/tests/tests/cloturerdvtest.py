# -*- coding: utf-8 -*-
from prestationtest import prestationTest
from administration.models import LettreCommande, clotureRdv
from datetime import date, datetime, timedelta

class clotureRdvTest(prestationTest):

       
   
       def test_Save(self):
              lc = LettreCommande.objects.create(site=self.site, marche=self.marche, charge_insertion=self.charge_insertion,\
                                            date_debut=date.today(), date_fin=date.today())
              cloture = clotureRdv.objects.create(lc=lc, dateheure=(datetime.today()+timedelta(days=1)))
              self.assertEqual(LettreCommande.CLOTURE, lc.avancement)
              

       def test_Delete(self):
              lc1 = LettreCommande.objects.create(site=self.site,\
                                                  marche=self.marche,\
                                                  charge_insertion=self.charge_insertion,\
                                                  date_debut=date.today(),\
                                                  date_fin=date.today())
              cloture = clotureRdv.objects.create(lc=lc1, dateheure=(datetime.today()+timedelta(days=1)))
              cloture.save()
              cloture.delete()
              self.assertEqual(LettreCommande.EN_ATTENTE, lc1.avancement)
              
              

                                            
       
   
