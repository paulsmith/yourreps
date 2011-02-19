#!/usr/bin/env python
import os.path
import re
import sys
from django.contrib.gis.gdal import DataSource
from django.contrib.humanize.templatetags.humanize import ordinal
from yourreps.models import District, Layer

class TigerImporter(object):
    def make_pretty_name(self, name):
        return '%s District' % ordinal(name)

    def valid_feature(self, feature):
        return True

    def iterfeatures(self, layer):
        for feature in layer:
            if self.valid_feature(feature):
                yield feature
        
    def import_shapefile(self, filename):
        layer = self.get_layer()
        ds = DataSource(filename)
        lyr = ds[0]
        for feature in self.iterfeatures(lyr):
            name = feature.get('NAME')
            # Strip leading zeros
            if name.startswith('0'):
                name = re.sub(r'^0+', '', name)
            district, created = District.objects.get_or_create(
                layer=layer,
                name=name,
                pretty_name=self.make_pretty_name(name),
                geom=feature.geom.geos,
            )
            if created:
                print 'created %s' % district

class StateSenateImporter(TigerImporter):
    def get_layer(self):
        layer, _ = Layer.objects.get_or_create(
            name = 'State Senate',
            honorific = 'Sen.'
        )
        return layer

    def valid_feature(self, feature):
        if feature.get('SLDU') == 'ZZZ':
            return False
        else:
            return True

class DelegateImporter(TigerImporter):
    def get_layer(self):
        layer, _ = Layer.objects.get_or_create(
            name = 'House of Delegates',
            honorific = 'Del.'
        )
        return layer

    def make_pretty_name(self, name):
        if re.match(r'\d+[a-zA-Z]+', name):
            return 'District %s' % name
        else:
            return TigerImporter.make_pretty_name(self, name)

    def valid_feature(self, feature):
        if feature.get('SLDL') == 'ZZZ':
            return False
        else:
            return True

class CongressImporter(TigerImporter):
    def get_layer(self):
        layer, _ = Layer.objects.get_or_create(
            name = 'U.S. Congress',
            honorific = 'Rep.'
        )
        return layer
            
importers = {
    'state-senate': StateSenateImporter,
    'delegate': DelegateImporter,
    'congress': CongressImporter,
}

def main():
    importer = importers[sys.argv[1]]()
    importer.import_shapefile(sys.argv[2])

if __name__ == '__main__':
    main()
