#!/usr/bin/env python

import re
import sys

from django.contrib.gis.gdal import DataSource
from django.contrib.humanize.templatetags.humanize import ordinal

from yourreps.models import District, Layer
import tiger

class Tiger2010Importer(tiger.TigerImporter):
    def get_layer(self):
        layer, _ = Layer.objects.get_or_create(
            name = self.layer_name,
            honorific = self.layer_honorific,
        )
        return layer

    def get_district_name(self, feature):
        fips = feature.get('STATEFP10')
        name = feature.get('GEOID10')[len(fips):]
        # Strip leading zeros
        if name.startswith('0'):
            name = re.sub(r'^0+', '', name)
        return name

    def import_shapefile(self, filename):
        layer = self.get_layer()
        ds = DataSource(filename)
        lyr = ds[0]
        for feature in self.iterfeatures(lyr):
            name = self.get_district_name(feature)
            district, created = District.objects.get_or_create(
                layer=layer,
                name=name,
                pretty_name=self.make_pretty_name(name),
                geom=feature.geom.geos,
            )
            if created:
                print 'created %s' % district

    def make_pretty_name(self, name):
        return '%s District' % ordinal(name)

class TexasHouseImporter(Tiger2010Importer):
    layer_name = 'Texas House of Representatives'
    layer_honorific = 'Rep.'

class TexasSenateImporter(Tiger2010Importer):
    layer_name = 'Texas Senate'
    layer_honorific = 'Sen.'

class TexasUSCongressImporter(Tiger2010Importer):
    layer_name = 'U.S. Congress'
    layer_honorific = 'Rep.'

    def get_district_name(self, feature):
        name = super(TexasUSCongressImporter, self).get_district_name(feature)
        return 'TX%s' % name

    def make_pretty_name(self, name):
        district_id = name[2:]
        name = super(TexasUSCongressImporter, self).make_pretty_name(district_id)
        return '%s of Texas' % name

importers = {
    'texas-house': TexasHouseImporter,
    'texas-senate': TexasSenateImporter,
    'us-congress': TexasUSCongressImporter,
}

def main():
    importer = importers[sys.argv[1]]()
    importer.import_shapefile(sys.argv[2])

if __name__ == '__main__':
    main()
