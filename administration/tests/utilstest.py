# -*- coding: utf-8 -*-
from django.test import TestCase
from greta.administration.pdf.utils import change_lines
import pdb

class UtilsTest(TestCase):

    def test_remove_endline_char_1(self):
        mutiline_string = "az\nzmfl\nekciov nfeoe, oez ekzf"
        expected_string = "az zmfl ekciov nfeoe, oez ekzf"
        self.assertEqual(expected_string, change_lines(mutiline_string))

    def test_remove_endline_char_2(self):
        mutiline_string = "az\rzmfl\rekciov nfeoe, oez ekzf"
        expected_string = "az zmfl ekciov nfeoe, oez ekzf"
        self.assertEqual(expected_string, change_lines(mutiline_string))

    def test_remove_all_endline_chars(self):
        mutiline_string = "az\rzmfl\rekci\rov nfeoe, oez ekzf"
        expected_string = "az zmfl ekci ov nfeoe, oez ekzf"
        self.assertEqual(expected_string, change_lines(mutiline_string))

    def test_insert_endline_char_1(self):
        long_string = "zef zefh zefh ezfh zefhzefh efh zefh mzf zefh zf zfh zefh zef zef zmej zef emfef emfh zeh e sqdhf azkfhr zkf zkefh zkefh kzeh kzefh aekzrfh aekzrjh akzerfh aekzrfh aekzrjfh "
        produced_string = change_lines(long_string)
        substrings = produced_string.split('\n')
        for substring in  substrings:
            self.assertTrue(len(substring) < 130)

    def test_insert_endline_char_2(self):
        long_string = "zef zefh zefh ezfh zefhzefh efh zefh mzf zefh zf zfh zefh zef zef zmej zef emfef emfh zeh e sqdhf azkfhr zkf zkefh zkefh kzeh kzefh aekzrfh aekzrjh akzerfh aekzrfh aekzrjfh qDEJKFH KZEFH ZKEsqdfh rzkfh kzre zkrhf ekrg ekmrjgh ekrgh ker kmrjhg aezrgjh ekrgjh eakmrjh ekmarjh ekmrajh mekarjh makerjhg aekmrjhg ekmarjhg ekarjhg kemarjh kmjhrg mrgh makjhr kmjhr mekrjhg ejkmrgh"
        produced_string = change_lines(long_string)
        substrings = produced_string.split('\n')
        for substring in  substrings:
            self.assertTrue(len(substring) < 130)

    """
    def test_real_data(self):
        real_string= u"La b\xe9n\xe9ficiaire ne parle pas le fran\xe7ais\r\net n'est pas mobile , elle n'est pas\r\nautonome par rapport aux transports en\r\ncommun et ne peux venir \xe0 Melun suivre\r\ndes cours de Fran\xe7ais Langue Etrang\xe8re\r\ndans une structure professionnelle.Elle\r\nne peut chercher un emploi que dans son\r\nquartier \xe0 c\xf4t\xe9 de chez elle. "
        
        produced_string = change_lines(real_string)
    """
