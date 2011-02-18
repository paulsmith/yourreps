import urllib
from django.contrib.gis.geos import fromstr
from django.shortcuts import render_to_response, redirect
from footprint.models import District
from footprint.geocode import geocode

def lookup(request):
    lnglat = request.GET.get('lnglat', '')
    if not lnglat:
        raise Http404()
    address = request.GET.get('address', '')
    bits = lnglat.split(',')
    pt = fromstr('POINT(%s %s)' % (bits[0], bits[1]))
    districts = District.objects.filter(geom__contains=pt).order_by('layer__order')
    map_query = {
        'center': '%s,%s' % (bits[1], bits[0]),
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
        'address': address,
    })

def search(request):
    q = request.GET.get('q')
    pt, address = geocode(q)
    if pt is None:
        raise Http404()
    lnglat = '%s,%s' % (pt.x, pt.y)
    params = {
        'lnglat': lnglat,
        'address': address
    }
    return redirect('/lookup/?' + urllib.urlencode(params))
