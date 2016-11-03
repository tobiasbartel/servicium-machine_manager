from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from instance_manager.models import Instance
from servicecatalog.models import ACCESS_DIRECTION, READ, WRITE, BOTH
from contact_manager.models import Contact

class NetworkZone(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    slug = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super(NetworkZone, self).save(*args, **kwargs)

    def __unicode__(self):
        return str("%s" % (self.name, ))

class HardwareType(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    slug = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super(HardwareType, self).save(*args, **kwargs)

    def __unicode__(self):
        return str("%s" % (self.name, ))


class PuppetRepo(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return str("%s" % (self.name,))


class MachineConnectMachine(models.Model):
    from_machine = models.ForeignKey('Machine', related_name='from_machine_relation')
    to_machine = models.ForeignKey('Machine', related_name='to_machine_relation')
    access_direction = models.CharField(choices=ACCESS_DIRECTION, default=BOTH, max_length=2)
    port = models.CharField(validators=[validate_comma_separated_integer_list],max_length=150,blank=True, null=True, default=None)
    comment = models.CharField(max_length=150, default=None, null=True, blank=True)

    class Meta:
        unique_together = ('from_machine', 'to_machine', 'access_direction', 'port')

    def __unicode__(self):
        return str("%s %s %s %s" % (self.from_machine, self.get_access_direction_display(), self.port, self.to_machine))


class Machine(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True, blank=False)
    type = models.ForeignKey(HardwareType, blank=False, related_name='type_of_machine')
    zone = models.ForeignKey(NetworkZone, blank=False, related_name='machine_in_nwzone')
    instance = models.ForeignKey(Instance, blank=False, null=False, related_name='machine_belongs_to_instance')
    owner = models.ForeignKey(Contact, blank=True, null=True, related_name='owner_of_machine')
    puppet_repo = models.ForeignKey(PuppetRepo, blank=True, related_name='puppet_for_machine')
    ip = models.GenericIPAddressField(blank=True, null=True)
    connected_to_machine = models.ManyToManyField('self', through='MachineConnectMachine', symmetrical=False, default=None, blank=True, related_name='machine_on_machine')
    customer_accesable = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        permissions = (
            ("is_owner", "Is Owner"),
        )
    def __unicode__(self)   :
        return str("%s - %s" % (self.name, self.instance))