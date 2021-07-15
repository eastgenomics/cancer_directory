from django.contrib import admin
from .models import (
    CancerType,
    ClinicalIndication,
    Scope,
    Technology,
    Target,
    GenomicTest,
    LinkTestToTarget,
    )


class CiAdmin(admin.ModelAdmin):
    list_display = (
        'cancer_id',
        'ci_code',
        'ci_name',
        )

    list_filter = ['cancer_id']


class GenomicTestAdmin(admin.ModelAdmin):
    list_display = (
        'ci_code',
        'test_code',
        'test_name',
        'target_string',
        'scope_id',
        'tech_id',
        'eligibility',
        )

    list_filter = ('scope_id', 'tech_id')


admin.site.register(CancerType)
admin.site.register(ClinicalIndication, CiAdmin)
admin.site.register(Scope)
admin.site.register(Technology)
admin.site.register(Target)
admin.site.register(GenomicTest, GenomicTestAdmin)
admin.site.register(LinkTestToTarget)
