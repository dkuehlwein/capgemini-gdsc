from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .forms import DataSciencesearch, Winnerselection
from .backendlogic import BackendLogic

# Create your views here.

def search(request):
    if request.POST:
        validationform = DataSciencesearch(request.POST)
        backendlogic = BackendLogic
        #pdffilenames = backendlogic.executemodel("Testing the logic gautam", "1", "P")
        pdffilenames = backendlogic.select2teams()
        #pdffilenames = ["BMW.pdf", "BAYER.pdf","GE.pdf",]
        context = {'result' :  pdffilenames}
        return render(request, 'DSCIV/result.html', context)
    else:
        return render(request, 'DSCIV/search.html')

def result(request):
    if request.POST:
        validationform = Winnerselection(request.POST)
        pdffilenames = [validationform.data,]
        context = {'result' :  pdffilenames}
        return render(request, 'DSCIV/test.html', context)
    else:
        return render(request, 'DSCIV/search.html')
