import pandas

from django.contrib.auth.models import User

from ngtdc_db.models import (CancerType, ClinicalIndication, Scope, Technology,
    Target, GenomicTest)


def insert_data(cleaned_data):
	"""Insert data into the database"""

	# Loop through each row
	for index, row in cleaned_data.iterrows():

		# Populate cancer types table
		cancer_type, created = CancerType.objects.get_or_create(
			cancer_type = row['cancer_type']
		)

		# Loop through row test scopes list to populate test scope table
		test_scope, created = Scope.objects.get_or_create(
			test_scope = row['test_scope']
		)

		# Loop through row technologies list to populate technology table
		technology, created = Technology.objects.get_or_create(
			technology = row['technology']
		)

		# Populate clinical indications table
		ci, created = ClinicalIndication.objects.get_or_create(
			cancer_type = cancer_type,
			ci_code = row['ci_code'],
			ci_name = row['ci_name']
		)

		# Populate genomic tests table
		genomic_test, created = GenomicTest.objects.get_or_create(
			ci_code = ci,
			test_code = row['test_code'],
			test_name = row['test_name'],

			targets = row['targets'],

			test_scope = test_scope,
			technology = technology,
			eligibility = row['eligibility'],
			)

		# Populate targets table and test-target link table
		for element in row['targets']:
			target, created = Target.objects.get_or_create(
				target = element
				)

			# link, created = LinkTestToTarget.objects.get_or_create(
			# 	test_code = row['test_code'],
			# 	test_target = target
			# 	)
