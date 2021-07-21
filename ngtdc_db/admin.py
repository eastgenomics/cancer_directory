from django.contrib import admin
from .models import (
	CancerTypeJul21,
	ClinicalIndicationJul21,
	SpecialistJul21,
	ScopeJul21,
	TechnologyJul21,
	InHouseTestJul21,
	CommissioningCategoryJul21,
	FamilyStructureJul21,
	CITTJul21,
	TTJul21,
	CurrentlyProvidedJul21,
	TargetJul21,
	GenomicTestJul21,
	EssentialTargetLinksJul21,
	DesirableTargetLinksJul21,

    CancerTypeNov20,
	ClinicalIndicationNov20,
	ScopeNov20,
	TechnologyNov20,
	InHouseTestNov20,
	CurrentlyProvidedNov20,
	TargetNov20,
	GenomicTestNov20,
	EssentialTargetLinksNov20,
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
        'inhouse_id',
        'eligibility',
        'provided_id',
        'family_id',
        'specialist_id',
        'cc_id',
        'citt_id',
        'tt_id',
        )
    filter_horizontal = ('targets_essential', 'targets_desirable')

    list_filter = (
        'scope_id',
        'tech_id',
        'inhouse_id',
        'provided_id',
        'family_id',
        )


admin.site.register(CancerTypeJul21)
admin.site.register(ClinicalIndicationJul21, CiAdmin)
admin.site.register(ScopeJul21)
admin.site.register(TechnologyJul21)
admin.site.register(InHouseTestJul21)
admin.site.register(CurrentlyProvidedJul21)
admin.site.register(TargetJul21)
admin.site.register(GenomicTestJul21, GenomicTestAdmin)
admin.site.register(SpecialistJul21)
admin.site.register(CommissioningCategoryJul21)
admin.site.register(FamilyStructureJul21)
admin.site.register(CITTJul21)
admin.site.register(TTJul21)
admin.site.register(EssentialTargetLinksJul21)
admin.site.register(DesirableTargetLinksJul21)

admin.site.register(CancerTypeNov20)
admin.site.register(ClinicalIndicationNov20)
admin.site.register(ScopeNov20)
admin.site.register(TechnologyNov20)
admin.site.register(InHouseTestNov20)
admin.site.register(CurrentlyProvidedNov20)
admin.site.register(TargetNov20)
admin.site.register(GenomicTestNov20)
admin.site.register(EssentialTargetLinksNov20)
