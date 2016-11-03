from django.contrib import admin
from machine_manager.models import *
from reversion_compare.admin import CompareVersionAdmin
from guardian.shortcuts import assign_perm, get_group_perms

class machine_to_machine(admin.TabularInline):
    model = MachineConnectMachine
    fk_name = 'from_machine'
    extra = 1


class NetworkZoneAdmin(CompareVersionAdmin):
    prepopulated_fields = { "slug": ("name",) }
admin.site.register(NetworkZone, NetworkZoneAdmin   )


class HardwareTypeAdmin(CompareVersionAdmin):
    prepopulated_fields = { "slug": ("name",) }
admin.site.register(HardwareType, HardwareTypeAdmin)


class PuppetRepoAdmin(CompareVersionAdmin):
    pass
admin.site.register(PuppetRepo, PuppetRepoAdmin)


class MachineAdmin(CompareVersionAdmin):
    inlines = (machine_to_machine, )

    def get_queryset(self, request):
        qs = super(MachineAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            for object in qs:
                keep = False
                for group in request.user.groups.all():
                    if u'is_owner' in get_group_perms(group, object):
                        keep = True
                if not keep:
                    qs = qs.exclude(pk=object.pk)
            return qs

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            my_group = request.user.groups.all().get(name__contains='TEAM_')
            assign_perm('is_owner', my_group, obj)
admin.site.register(Machine, MachineAdmin)