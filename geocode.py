import json
import urllib
from django.contrib.gis.geos import fromstr

def geocode(q):
    query = {
        'address': q,
        'sensor': 'false',
    }
    url = 'http://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(query)
    f = urllib.urlopen(url)
    result = json.loads(f.read())
    if result['status'] == 'OK':
        location = result['results'][0]['geometry']['location']
        pt = fromstr('POINT(%s %s)' % (location['lng'], location['lat']))
        return pt
