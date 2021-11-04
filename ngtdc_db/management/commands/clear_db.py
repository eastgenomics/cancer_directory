#!usr/bin/env python

"""
Clears all records from all models in the database.
"""


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
    help = "Clear all records from all models in the database."

    def handle(self, *args, **kwargs):

        # Specify all models of the database
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

        # Delete all records in each model
        for model in models:
            model.objects.all().delete()
