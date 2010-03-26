from datetime import datetime
import time 
from django.template import Context, loader
from django.shortcuts import render_to_response
from greta.administration.models import LettreCommande

def sortie(request):
    all_lc = LettreCommande.objects.all()
    #t = loader.get_template('sortie.html')
    #output = ','.join([str(lc.date_debut) for lc in all_lc])
    c = Context({
        'all_lc': all_lc,
    })
    #return HttpResponse(t.render(c))
    #return HttpResponse(output)
    return render_to_response('sortie.html', {'all_lc': all_lc})


def formstat(request):
    return render_to_response('formstat.html')

def result(request):
    try:
        date = request.POST['date']       

    except (KeyError):
        pass
    else:
        date = datetime(*(time.strptime(date,"%Y-%m-%d")[0:6])).date()
        lc = LettreCommande.objects.filter(date_cloture_lt=date)
    
    return render_to_response('result.html')
