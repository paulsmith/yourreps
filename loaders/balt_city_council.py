#!/usr/bin/env python
"""
Shapefile from data.baltimorecity.gov
"""
import os.path
import sys
from django.contrib.gis.gdal import DataSource
from django.contrib.humanize.templatetags.humanize import ordinal
from yourreps.models import Layer, District

def import_city_council(filename):
    ds = DataSource(filename)
    lyr = ds[0]
    layer, _ = Layer.objects.get_or_create(
        name='Baltimore City Council'
    )
    for feature in lyr:
        name = feature.get('AREA_NAME')
        district, created = District.objects.get_or_create(
            layer = layer,
            name = name,
            pretty_name = '%s District' % ordinal(name),
            geom = feature.geom.geos
        )
        if created:
            print 'created', district

def main():
    import_city_council(sys.argv[1])

if __name__ == '__main__':
    main()
