from django.test import TestCase
from greta.administration.csv.csvResponse import period 
from datetime import date, timedelta


class periodTest(TestCase):

    def setUp(self):
       pass
    
    def test_disjoins1(self):
        p1 = period(date(day=1, month=2, year=2008), date(day=28, month=2, year=2008))
        p2 = period(date(day=1, month=2, year=2009), date(day=28, month=2, year=2009))
        self.assertTrue(p1.disjoin(p2))
        
    def test_disjoins2(self):
        p1 = period(date(day=1, month=2, year=2008), date(day=28, month=2, year=2008))
        p2 = period(date(day=1, month=2, year=2008), date(day=28, month=2, year=2009))
        self.assertFalse(p1.disjoin(p2))
    
    def test_empty_intersection1(self):
        p1 = period(date(day=1, month=2, year=2008), date(day=28, month=2, year=2008))
        p2 = period(date(day=1, month=2, year=2009), date(day=28, month=2, year=2009))
        self.assertEqual(timedelta(), p1.intersection(p2))
        
    def test_nonempty_intersection2(self):
        p1 = period(date(day=1, month=2, year=2008), date(day=28, month=2, year=2008))
        p2 = period(date(day=26, month=2, year=2008), date(day=28, month=2, year=2009))
        self.assertEqual(timedelta(days=3), p1.intersection(p2))
            
    def test_same_ensemble(self):
        p1 = period(date(day=1, month=2, year=2008), date(day=28, month=2, year=2008))
        p2 = period(date(day=1, month=2, year=2008), date(day=28, month=2, year=2008))
        self.assertEqual(timedelta(days=28), p1.intersection(p2))
        
    def test_sous_ensemble(self):
        p1 = period(date(day=1, month=2, year=2008), date(day=28, month=2, year=2009))
        p2 = period(date(day=1, month=4, year=2008), date(day=3, month=4, year=2008))
        self.assertEqual(timedelta(days=3), p1.intersection(p2))


   