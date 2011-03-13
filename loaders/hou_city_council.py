#!/usr/bin/env python
"""
Loader for Houston, Texas City Council boundaries

Using shapefile from Harris County Public Infrastructure GIS:
http://www.eng.hctx.net/GIS/gis.htm

"""
import sys
from django.contrib.gis.gdal import CoordTransform, DataSource
from django.db import connections, DEFAULT_DB_ALIAS
from yourreps.models import Layer, District


def import_city_council(filename):
    ds = DataSource(filename)
    lyr = ds[0]
    layer, _ = Layer.objects.get_or_create(
        name='Houston City Council'
    )
    SpatialRefSys = connections[DEFAULT_DB_ALIAS].ops.spatial_ref_sys()
    target_srid = District._meta.get_field('geom').srid
    target_srs = SpatialRefSys.objects.get(srid=target_srid).srs
    coord_transform = CoordTransform(lyr.srs, target_srs)
    for feature in lyr:
        name = feature.get('DISTRICT')
        geom = feature.geom.transform(coord_transform, clone=True)
        district, created = District.objects.get_or_create(
            layer = layer,
            name = name,
            pretty_name = 'District %s' % name,
            geom = geom.geos
        )
        if created:
            print 'created', district

def main():
    import_city_council(sys.argv[1])

if __name__ == '__main__':
    main()
