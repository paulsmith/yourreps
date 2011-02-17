import urllib
from django.shortcuts import render_to_response
from footprint.models import District
from footprint.geocode import geocode

def footprint(request):
    q = request.GET.get('q')
    pt = geocode(q)
    if pt is None:
        raise Http404()
    districts = District.objects.filter(geom__contains=pt).order_by('layer__order')
    map_query = {
        'center': q,
        #'zoom': 14,
        'size': '240x388',
        'maptype': 'roadmap',
        'markers': '%s,%s' % (pt.y, pt.x),
        'sensor': 'false',
    }
    map_url = 'http://maps.google.com/maps/api/staticmap?' + urllib.urlencode(map_query)
    return render_to_response('footprint.html', {
        'point': pt,
        'districts': districts,
        'map_url': map_url,
    })
