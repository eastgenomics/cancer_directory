# from django.contrib import admin
# from .models import (
#     CancerType,
#     ClinicalIndication,
#     Specialist,
#     Scope,
#     Technology,
#     InHouseTest,
#     CommissioningCategory,
#     FamilyStructure,
#     CITT,
#     TT,
#     CurrentlyProvided,
#     Target,
#     GenomicTest,
#     EssentialTargetLinks,
#     DesirableTargetLinks,
#     )


# class CiAdmin(admin.ModelAdmin):
#     list_display = (
#         'cancer_id',
#         'ci_code',
#         'ci_name',
#         )

#     list_filter = ['cancer_id']


# class GenomicTestAdmin(admin.ModelAdmin):
#     list_display = (
#         'ci_code',
#         'test_code',
#         'test_name',
#         'scope_id',
#         'tech_id',
#         'inhouse_id',
#         'eligibility',
#         'provided_id',
#         'family_id',
#         'specialist_id',
#         'cc_id',
#         'citt_id',
#         'tt_id',
#         )
#     filter_horizontal = ('targets_essential', 'targets_desirable')

#     list_filter = (
#         'scope_id',
#         'tech_id',
#         'inhouse_id',
#         'provided_id',
#         'family_id',
#         )


# admin.site.register(CancerType)
# admin.site.register(ClinicalIndication, CiAdmin)
# admin.site.register(Scope)
# admin.site.register(Technology)
# admin.site.register(InHouseTest)
# admin.site.register(CurrentlyProvided)
# admin.site.register(Target)
# admin.site.register(GenomicTest, GenomicTestAdmin)
# admin.site.register(Specialist)
# admin.site.register(CommissioningCategory)
# admin.site.register(FamilyStructure)
# admin.site.register(CITT)
# admin.site.register(TT)
# admin.site.register(EssentialTargetLinks)
# admin.site.register(DesirableTargetLinks)
