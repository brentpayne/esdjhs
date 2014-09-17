from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.shortcuts import render
from advisors.search_indexes import AdvisorIndex


def first_name_search(request, first_name):
    context = dict(first_name=first_name)
    san_diego = Point(-118.15725509999999, 32.7153292)
    nyc = Point(-74.0359, 40.7227)
    # Within a two miles.
    max_dist = D(mi=20000)
    context['point'] = nyc
    context['view_x'] = nyc.get_x()
    context['view_y'] = nyc.get_y()
    context['mapbox_token'] = settings.MAPBOX_TOKEN
    context['mapbox_id'] = settings.MAPBOX_MAPID
    context['advisors'] = AdvisorIndex.objects.filter(first_name=first_name).dwithin('location', nyc, max_dist)[:20]
    return render(request, 'advisors/first_name_search.html', context)
