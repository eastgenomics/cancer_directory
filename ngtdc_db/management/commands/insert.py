import pandas
from django.contrib.auth.models import User

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


def insert_data(cleaned_data):
	"""Insert data into the database"""

	# Loop through each row
	for index, row in cleaned_data.iterrows():

		# Populate cancer types table
		cancer_type, created = CancerType.objects.get_or_create(
			cancer_type = row['cancer_type'],
		)

		# Populate test scopes table
		test_scope, created = Scope.objects.get_or_create(
			test_scope = row['test_scope'],
		)

		# Populate technologies table
		technology, created = Technology.objects.get_or_create(
			technology = row['technology'],
		)

		# Populate in-house tests table
		inhouse, created = InHouseTest.objects.get_or_create(
			inhouse = row['in_house_test'],
		)

		# Populate currently provided table
		provided, created = CurrentlyProvided.objects.get_or_create(
			provided = row['currently_provided'],
		)

		# Populate clinical indications table
		ci, created = ClinicalIndication.objects.get_or_create(
			cancer_id = cancer_type,
			ci_code = row['ci_code'],
			ci_name = row['ci_name'],
		)

		# Populate genomic tests table
		genomic_test, created = GenomicTest.objects.get_or_create(
			ci_code = ci,
			test_code = row['test_code'],
			test_name = row['test_name'],
			scope_id = test_scope,
			tech_id = technology,
			inhouse_id = inhouse,
			eligibility = row['eligibility'],
			provided_id = provided,
			)

		# Populate target and LinkTestToTarget tables
		for element in row['targets']:
			target, created = Target.objects.get_or_create(
				target = element,
				)

			link, created = LinkTestToTarget.objects.get_or_create(
				test_code = genomic_test,
				target_id = target,
				)
