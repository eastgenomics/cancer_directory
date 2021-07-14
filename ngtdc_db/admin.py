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
    list_display = ('cancer_type', 'ci_code', 'ci_name')
    list_filter = ['cancer_type']


class GenomicTestAdmin(admin.ModelAdmin):
    list_display = ('ci_code', 'test_code', 'test_name', 'target_string',
        'test_scope', 'technology', 'eligibility')
    list_filter = ('test_scope', 'technology')


admin.site.register(CancerType)
admin.site.register(ClinicalIndication, CiAdmin)
admin.site.register(Scope)
admin.site.register(Technology)
admin.site.register(Target)
admin.site.register(GenomicTest, GenomicTestAdmin)
admin.site.register(LinkTestToTarget)
