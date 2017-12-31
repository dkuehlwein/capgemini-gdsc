from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponse, HttpResponseRedirect

# Create your views here.

def search(request):
    if request.GET:
        pdffilenames = ["BMW.pdf", "BAYER.pdf","GE.pdf",]
        context = {'result' :  pdffilenames}
        #return render_to_response('DSCIV/search.html', result)
        return render(request, 'DSCIV/search.html', context)
    else:
        return render(request, 'DSCIV/search.html')
