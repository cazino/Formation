from django.db import models
from greta.administration import params

class Marche(models.Model):

    class Meta:
        app_label = 'administration'
        verbose_name = "Marché"
        verbose_name_plural = "Marchés"
        ordering = ['polemploi_id']

    polemploi_id = models.SlugField(u"Numéro de marché", max_length=50)
    montant_unitaire = models.FloatField(u"Montant unitaire")
    portage = models.FloatField(u"Portage (% nombre entier)")
    
    def __unicode__(self):
        return "%s" % (self.polemploi_id)

    def montantjour(self):
        return self.montant_unitaire/float(params.duree_lc) 
