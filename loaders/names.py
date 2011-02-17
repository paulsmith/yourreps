import json
import sys

from footprint.models import Layer, District, Representative

def load_names(layer, filename):
    reps = json.load(open(filename))
    for rdict in reps:
        district = District.objects.get(layer=layer, name=rdict['district'])
        try:
            party = rdict['party']
        except KeyError:
            party = 'D'
        rep, created = Representative.objects.get_or_create(
            district = district,
            name = rdict['name'],
            url = rdict['url'],
            party = party
        )
        if created:
            print >> sys.stderr, 'created', rep

def main():
    if len(sys.argv[1:]) < 1:
        for layer in Layer.objects.all():
            print >> sys.stderr, layer, layer.id
        sys.exit(1)
    layer = Layer.objects.get(id=sys.argv[1])
    load_names(layer, sys.argv[2])

if __name__ == '__main__':
    main()
