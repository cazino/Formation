from __future__ import with_statement
import sys, os, pdb
from django.core.management import setup_environ

project_path = "/home/kazou/dev"
sys.path.append(project_path)
from greta import settings
setup_environ(settings)


fixture_filepath = settings.PROJECT_PATH + "/administration/models/fixtures/bilan1.json"

from greta.administration.models import LettreCommande, Marche, ChargeInsertion , Site, Prestataire
from django.core.serializers import json
serializer = json.Serializer()
lc_queryset =  LettreCommande.objects.filter(pk=315)
lc = lc_queryset.get()
marche = Marche.objects.get(pk=lc.marche.pk)
charge_insertion = ChargeInsertion.objects.get(pk=lc.charge_insertion.pk)
sites = list(charge_insertion.les_sites.all())
sites.append(lc.site)
prestataires = list(Prestataire.objects.filter(pk__in=[site.prestataire.pk for site in sites]))
final_list = [marche, prestataires, sites, charge_insertion, lc]

to_serialize = []
for item in final_list:
    if isinstance(item, list):
        to_serialize.extend(item)
    else:
        to_serialize.append(item)
        
    
with open(fixture_filepath,'w') as f:
        f.write(serializer.serialize(to_serialize, indent=4))

