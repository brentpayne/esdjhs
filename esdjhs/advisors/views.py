from django.shortcuts import render
from advisors.search_indexes import AdvisorIndex


def first_name_search(request, first_name):
    context = dict(first_name=first_name)
    context['advisors'] = AdvisorIndex.objects.filter(first_name=first_name)[:5]
    return render(request, 'advisors/first_name_search.html', context)
