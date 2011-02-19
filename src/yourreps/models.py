from django.contrib.gis.db import models

class Layer(models.Model):
    name = models.CharField(max_length=200)
    honorific = models.CharField('Honorific (abbrev.)', max_length=10, blank=True, null=True)
    order = models.IntegerField('Display order', null=True)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name

class District(models.Model):
    layer = models.ForeignKey(Layer)
    name = models.CharField(max_length=10)
    pretty_name = models.CharField(max_length=200)
    geom = models.GeometryField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return '%s %s' % (self.layer, self.name)

class Representative(models.Model):
    district = models.ForeignKey(District, related_name='representatives')
    name = models.CharField(max_length=200)
    party = models.CharField(max_length=1)
    url = models.CharField('URL', max_length=255)

    def __unicode__(self):
        return self.pretty_name

    @property
    def honorific(self):
        return self.district.layer.honorific

    @property
    def pretty_name(self):
        if self.honorific:
            return '%s %s (%s)' % (self.honorific, self.name, self.party)
        else:
            return '%s (%s)' % (self.name, self.party)
