from django.contrib import admin
from .models import (
	CancerType,
	ClinicalIndication,
	TestScope,
	Technology,
	Target,
	GenomicTest,
	EssentialTarget,
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
        'scope_id',
        'tech_id',
        'eligibility',
        'currently_provided',
        'inhouse_technology',
        )
        
    filter_horizontal = ('targets_essential',)

    list_filter = (
        'scope_id',
        'tech_id',
        'inhouse_technology',
        'currently_provided',
        )


admin.site.register(CancerType)
admin.site.register(ClinicalIndication, CiAdmin)
admin.site.register(GenomicTest, GenomicTestAdmin)
admin.site.register(TestScope)
admin.site.register(Technology)
admin.site.register(Target)
admin.site.register(EssentialTarget)
