from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from youthPlatform.models import JobAd, Qualification

# Create your views here.


# our search result view, which is universally applicable for searching
# all the things like jobs or trainings or ideas
class Search(View):
    model = None
    def __init__(self, model):
        model = model
        self.model = model

    def get(self, request):
        try:
            queryString = request.GET.get('query')
        except:
            queryString = None

        if queryString==None:
            # just show the results, no need of any filters
            results = self.model.objects.order_by('-priority')
        else:
            # match the querystring also
            quals = Qualification.objects.filter(level=queryString.capitalize())
            q = Q()
            for x in quals:
                q|=Q(qualification=x)
            
            results = self.model.objects.filter(q)# |
                    #Q(institutionLocation__contains=queryString) |
                    #Q(institutionDistrict__contains=queryString) )

        # now pagination
        paginator = Paginator(results, 10) # show 10 per page
        page = request.GET.get('page')

        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        error = None
        if len(result)==0:
            error = "No results found"

        context = {'results':result, 'error':error}
        return render(request, 'youthPlatform/search.html', context)

