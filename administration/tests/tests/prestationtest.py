# -*- coding: utf-8 -*-
from django.test import TestCase
from administration.models import Marche, ChargeInsertion, Prestataire, Site
from datetime import date, datetime, timedelta

class prestationTest(TestCase):

       def setUp(self):
              self.marche = Marche.objects.create(polemploi_id='idmarche', portage=0.3, montant_unitaire=0.2)
              self.prestataire = Prestataire.objects.create(nom='prestataire')
              self.site = Site.objects.create(nom='prestataire-site', prestataire=self.prestataire)
              
              self.charge_insertion = ChargeInsertion.objects.create(nom="nom", prenom="prénom")
              self.charge_insertion.les_sites.add(self.site)
              self.charge_insertion.save()
              

   
       
