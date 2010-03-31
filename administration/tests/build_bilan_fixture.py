from __future__ import with_statement
import sys, os, pdb
from django.core.management import setup_environ

project_path = "/home/kazou/dev"
sys.path.append(project_path)
from greta import settings
setup_environ(settings)


from optparse import OptionParser
import pdb

# Command line options                                                                                                                                       
parser = OptionParser()
parser.add_option("-f", "--file", action="store", type="string", dest="filename")
parser.add_option("-l", "--lc", action="store", dest="int", dest="lc_pk")
opts, args = parser.parse_args()


fixture_filepath = settings.PROJECT_PATH + "/administration/models/fixtures/" + opts.filename + '.json'

from greta.administration.models import LettreCommande, Marche, ChargeInsertion , Site, Prestataire
from greta.administration.models import Rdv
from django.core.serializers import json
from django.core.exceptions import ObjectDoesNotExist


serializer = json.Serializer()
lc_queryset =  LettreCommande.objects.filter(pk=opts.lc_pk)
lc = lc_queryset.get()
marche = Marche.objects.get(pk=lc.marche.pk)
charge_insertion = ChargeInsertion.objects.get(pk=lc.charge_insertion.pk)
sites = list(charge_insertion.les_sites.all())
sites.append(lc.site)
prestataires = list(Prestataire.objects.filter(pk__in=[site.prestataire.pk for site in sites]))
rdvs = list(lc.rdv.all())


final_list = [marche, prestataires, sites, charge_insertion, lc, lc.ouverture_rdv, rdvs, lc.etat_civil]
#final_list = final_list + [lc.situation_sociopro, ]#lc.frein, lc.bilan, lc.cloture]
for item in ['frein',' bilan', 'cloture', 'situation_sociopro']:
    try:
        final_list.append(eval("lc.%s" % (item,)))
    except ObjectDoesNotExist:
        pass
        
to_serialize = []
for item in final_list:
    if isinstance(item, list):
        to_serialize.extend(item)
    else:
        to_serialize.append(item)
        
    
with open(fixture_filepath,'w') as f:
        f.write(serializer.serialize(to_serialize, indent=4, ensure_ascii=False).encode('utf-8'))


