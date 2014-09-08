from django.shortcuts import render

def first_name_search(request, first_name):
    context = dict(first_name=first_name)
    return render(request, 'advisors/first_name_search.html', context)
