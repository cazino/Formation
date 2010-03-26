# -*- coding: utf-8 -*-
from datetime import date
from django.test import TestCase
from greta.administration.admin import Feries, intervalle


class FeriesPaquesTest(TestCase):
      
    def test_paques_2009(self):
        feries = Feries(year=2009)
        paques_2009 = date(day=13, month=4, year=2009)
        self.assertEqual(paques_2009, feries.paques_oudin())
        
    def test_paques_2010(self):
        feries = Feries(year=2010)
        paques_2010 = date(day=5, month=4, year=2010)
        self.assertEqual(paques_2010, feries.paques_oudin())
        
    def test_feries_2009(self):
        year = 2009
        feries = Feries(year=year)
        expected_feries = [date(day=1, month=1, year=year),
                           date(day=13, month=4, year=year),
                           date(day=1, month=5, year=year),
                           date(day=8, month=5, year=year),
                           date(day=21, month=5, year=year),
                           date(day=1, month=6, year=year),
                           date(day=14, month=7, year=year),
                           date(day=15, month=8, year=year),
                           date(day=1, month=11, year=year),
                           date(day=11, month=11, year=year),
                           date(day=25, month=12, year=year),
                           ]
        caculated_feries = feries.feries()
        self.assertEqual(expected_feries, caculated_feries)
        
    def test_feries_2010(self):
        year = 2010
        feries = Feries(year=year)
        expected_feries = [date(day=1, month=1, year=year),
                           date(day=5, month=4, year=year),
                           date(day=1, month=5, year=year),
                           date(day=8, month=5, year=year),
                           date(day=13, month=5, year=year),
                           date(day=24, month=5, year=year),
                           date(day=14, month=7, year=year),
                           date(day=15, month=8, year=year),
                           date(day=1, month=11, year=year),
                           date(day=11, month=11, year=year),
                           date(day=25, month=12, year=year),
                           ]
        caculated_feries = feries.feries()
        self.assertEqual(expected_feries, caculated_feries)
        
class IntervalleTest(TestCase):
    
    def test_interval_dummy_1_day(self):
        year = 2009
        first_date = date(day=2, month=1, year=year)
        new_date = date(day=3, month=1, year=year)
        self.assertEqual(1, intervalle(first_date, new_date))
    
    def test_interval_dummy_2_day(self):
        year = 2009
        first_date = date(day=2, month=1, year=year)
        new_date = date(day=4, month=1, year=year)
        self.assertEqual(2, intervalle(first_date, new_date))
        
    def test_interval_with_one_ferie(self):
        year = 2009
        first_date = date(day=2, month=7, year=year)
        new_date = date(day=15, month=7, year=year)
        self.assertEqual(12, intervalle(first_date, new_date))
        
    def test_interval_with_one_ferie_over_two_years(self):
        first_date = date(day=31, month=12, year=2008)
        new_date = date(day=3, month=1, year=2009)
        self.assertEqual(2, intervalle(first_date, new_date))
