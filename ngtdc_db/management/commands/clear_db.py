from django.core.management.base import BaseCommand

from ngtdc_db.models import (
    CancerType,
    ClinicalIndication,
    Specialist,
    Scope,
    Technology,
    InHouseTest,
    CommissioningCategory,
    FamilyStructure,
    CITT,
    TT,
    CurrentlyProvided,
    Target,
    GenomicTest,
    EssentialTargetLinks,
    DesirableTargetLinks,
	)


class Command(BaseCommand):
    help = "Clear all database records"

    def handle(self, *args, **kwargs):
        models = [
            CancerType,
            ClinicalIndication,
            Specialist,
            Scope,
            Technology,
            InHouseTest,
            CommissioningCategory,
            FamilyStructure,
            CITT,
            TT,
            CurrentlyProvided,
            Target,
            GenomicTest,
            EssentialTargetLinks,
            DesirableTargetLinks,
            ]

        for model in models:
            model.objects.all().delete()
