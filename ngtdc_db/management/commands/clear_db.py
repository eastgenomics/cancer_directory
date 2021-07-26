from django.core.management.base import BaseCommand

from ngtdc_db.models import (
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


class Command(BaseCommand):
    help = "Clear all database records"

    def handle(self, *args, **kwargs):
        models = [
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
            ]

        for model in models:
            model.objects.all().delete()
