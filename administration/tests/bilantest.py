from __future__ import with_statement
import pdb
from django.test import TestCase
from django.test.client import Client
from django.http import HttpResponse
from greta.administration.models import LettreCommande, Marche
from greta.administration.pdf.bilanPdf import bilanDoc


class BilanTest(TestCase):

    fixtures = ['bilan315.json', 'bilan3030.json', 'bilan961.json']

    def setUp(self):
        pass

    def test_315(self):
        # '&' bug
        response = HttpResponse()
        bilanDoc(response, LettreCommande.objects.get(pk=315)).buildDoc()
        self.assertTrue(True)

    def test_3030(self):
        # Ok no Bug
        response = HttpResponse()
        bilanDoc(response, LettreCommande.objects.get(pk=3030)).buildDoc()
        self.assertTrue(True)

    def test_961(self):
        # No LC number bug
        response = HttpResponse()
        bilanDoc(response, LettreCommande.objects.get(pk=961)).buildDoc()
        self.assertTrue(True)








