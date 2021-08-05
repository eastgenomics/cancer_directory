from django.contrib import admin
from .models import (
	CancerType,
	ClinicalIndication,
	SpecialistTestGroup,
	TestScope,
	Technology,
	CommissioningCategory,
	OptimalFamilyStructure,
	CITTComment,
	Target,
	GenomicTest,
	EssentialTarget,
	DesirableTarget,
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
        'inhouse_technology',
        'eligibility',
        'currently_provided',
        'family_id',
        'specialist_id',
        'cc_id',
        'citt_id',
        'tt_code',
        )
        
    filter_horizontal = ('targets_essential', 'targets_desirable')

    list_filter = (
        'scope_id',
        'tech_id',
        'inhouse_technology',
        'currently_provided',
        'family_id',
        )


admin.site.register(CancerType)
admin.site.register(ClinicalIndication, CiAdmin)
admin.site.register(GenomicTest, GenomicTestAdmin)
admin.site.register(TestScope)
admin.site.register(Technology)
admin.site.register(Target)
admin.site.register(EssentialTarget)
admin.site.register(DesirableTarget)
admin.site.register(SpecialistTestGroup)
admin.site.register(CommissioningCategory)
admin.site.register(OptimalFamilyStructure)
admin.site.register(CITTComment)
