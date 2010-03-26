from django.test import TestCase
from greta.administration.stat.stat import StatResult 



class StatResultTest(TestCase):

    def setUp(self):
       result = StatResult() 
        
    def test_init(self):
        pass

    def test_empty_comparaison(self):
        result1 = StatResult()
        result2 = StatResult()
        self.assert_(result1 == result2)
        
    def test_false_comparaison(self):
        result1 = StatResult()
        result2 = StatResult()
        result2.premier_rdv_absent = 1
        self.assertFalse(result1 == result2)
        
        
    

   