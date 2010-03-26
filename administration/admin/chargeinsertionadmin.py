from django.contrib import admin
from greta.administration.models import ChargeInsertion



class chargeInsertionAdmin(admin.ModelAdmin):

    list_display = ('nom', 'prenom', 'tel_fixe', 'lc_actif', 'lc_attente')
    search_fields = ['nom', 'prenom']
    ordering = ['nom',]
    
    
admin.site.register(ChargeInsertion,chargeInsertionAdmin)
