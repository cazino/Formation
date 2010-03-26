# -*- coding: utf-8 -*-
from prestationtest import prestationTest
from administration.models import LettreCommande, ouvertureRdv, models_etat
from datetime import date, datetime

class ouvertureRdvTest(prestationTest):

    def build_LC_Rdv(self,rdvStatut):
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=date.today(),\
                                            date_fin=date.today())
        return (lc1, ouvertureRdv.objects.create(lettre_commande=lc1, dateheure=datetime.today(), statut=rdvStatut))

    def test_save(self):
        
        today_date = date.today()
        today_datetime = datetime.today()
        statutest = u'Présent contractualisé'
        lc1 = LettreCommande.objects.create(marche=self.marche,\
                                            charge_insertion=self.charge_insertion,\
                                            site=self.site,\
                                            date_debut=today_date,\
                                            date_fin=today_date)
        rdv = ouvertureRdv.objects.create(lettre_commande=lc1, dateheure=today_datetime, statut=statutest)
        rdv.save()
        rdv = ouvertureRdv.objects.get(pk=rdv.pk)

        
        self.assertEqual(lc1,rdv.lettre_commande)
        #self.assertEqual(today_datetime,rdv.dateheure)
        self.assertEqual(statutest,rdv.statut)


    def test_Report(self):
        (lc1, rdv) = self.build_LC_Rdv(ouvertureRdv.REPORT)
        self.assertEqual(models_etat.LC_ANNULE, lc1.avancement)
        
    def test_Present_Contractualise(self):
        (lc1, rdv) = self.build_LC_Rdv(ouvertureRdv.PRESENT_C)
        self.assertEqual(models_etat.LC_EN_COURS, lc1.avancement)

    def test_Absent(self):
        (lc1, rdv) = self.build_LC_Rdv(ouvertureRdv.ABSENT)
        self.assertEqual(models_etat.LC_ANNULE, lc1.avancement)
        
    def test_Present_Pas_Contractualise(self):
        (lc1, rdv) = self.build_LC_Rdv(ouvertureRdv.PRESENT_NC)
        self.assertEqual(models_etat.LC_ANNULE, lc1.avancement)

    def test_Delete_1(self):
        (lc1, rdv) = self.build_LC_Rdv(ouvertureRdv.PRESENT_NC)
        rdv.delete()
        self.assertEqual(models_etat.LC_EN_ATTENTE, lc1.avancement)

    def test_Delete_2(self):
        (lc1, rdv) = self.build_LC_Rdv(ouvertureRdv.PRESENT_C)
        rdv.delete()
        self.assertEqual(models_etat.LC_EN_ATTENTE, lc1.avancement)

    def test_Delete_3(self):
        (lc1, rdv) = self.build_LC_Rdv(ouvertureRdv.REPORT)
        rdv.delete()
        self.assertEqual(models_etat.LC_EN_ATTENTE, lc1.avancement)

    def test_Delete_4(self):
        (lc1, rdv) = self.build_LC_Rdv(ouvertureRdv.ABSENT)
        rdv.delete()
        self.assertEqual(models_etat.LC_EN_ATTENTE, lc1.avancement)
            












        

