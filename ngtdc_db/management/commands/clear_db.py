from django.core.management.base import BaseCommand

from ngtdc_db.models import (
	CancerType,
	ClinicalIndication,
	Scope,
	Technology,
    InHouseTest,
    CurrentlyProvided,
    Target,
	GenomicTest,
	LinkTestToTarget,
	)


class Command(BaseCommand):
    help = "Clear all database records"

    def handle(self, *args, **kwargs):
        models = [
            CancerType,
            ClinicalIndication,
            Scope,
            Technology,
            InHouseTest,
            CurrentlyProvided,
            Target,
            GenomicTest,
            LinkTestToTarget,
            ]

        for model in models:
            model.objects.all().delete()
