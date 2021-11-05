#!usr/bin/env python

"""
Clears all records from all models in the database.

If you will be making any changes to the database models, do that BEFORE
running this. Make any changes to models, update the other files in the app
accordingly, and make/apply migrations. THEN you can clear the database to
repopulate.

"""


from django.core.management.base import BaseCommand

from ngtdc_db.models import (
    CancerType,
	ClinicalIndication,
	TestScope,
	Technology,
	Target,
	GenomicTest,
	EssentialTarget,
	)


class Command(BaseCommand):
    help = "Clear all records from all models in the database."

    def handle(self, *args, **kwargs):

        # Specify all models of the database
        models = [
            CancerType,
            ClinicalIndication,
            TestScope,
            Technology,
            Target,
            GenomicTest,
            EssentialTarget,
            ]

        # Delete all records in each model
        for model in models:
            model.objects.all().delete()
