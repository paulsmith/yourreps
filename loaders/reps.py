#!/usr/bin/env python
import json
import sys
from yourreps.models import Representative, District

def import_reps(filename, district_slug):
    district = District.objects.get(slug=district_slug)
    reps = json.load(open(filename))
    for rep_dict in reps:
        try:
            party = rep['name']
        except KeyError:
            party = 'D'
        rep, created = Representative.objects.get_or_create(
            district = district,
            name = rep['name'],
            party = party
        )
        if created:
            print 'created', rep

def main():
    import_reps(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
