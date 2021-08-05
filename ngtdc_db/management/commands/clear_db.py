from django.core.management.base import BaseCommand

from ngtdc_db.models import (
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


class Command(BaseCommand):
    help = "Clear all database records"

    def handle(self, *args, **kwargs):
        models = [
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
            ]

        for model in models:
            model.objects.all().delete()
