import pandas
from django.contrib.auth.models import User

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

import httplib2 as http
import json
from ratelimit import limits

try:
    from urlparse import urlparse

except ImportError:
    from urllib.parse import urlparse


def insert_data(cleaned_data, directory_version):
	"""Insert data into the database"""

	for index, row in cleaned_data.iterrows():

		if directory_version == '1':
			# Populate cancer types table
			cancer_type, created = CancerTypeNov20.objects.get_or_create(
				cancer_type = row['cancer_type'],
			)

			# Populate test scopes table
			test_scope, created = ScopeNov20.objects.get_or_create(
				test_scope = row['test_scope'],
			)

			# Populate technologies table
			technology, created = TechnologyNov20.objects.get_or_create(
				technology = row['technology'],
			)

			# Populate in-house tests table
			inhouse, created = InHouseTestNov20.objects.get_or_create(
				inhouse = row['in_house_test'],
			)

			# Populate currently provided table
			provided, created = CurrentlyProvidedNov20.objects.get_or_create(
				provided = row['currently_provided'],
			)

			# Populate clinical indications table
			ci, created = ClinicalIndicationNov20.objects.get_or_create(
				cancer_id = cancer_type,
				ci_code = row['ci_code'],
				ci_name = row['ci_name'],
			)

			# Populate genomic tests table
			genomic_test, created = GenomicTestNov20.objects.get_or_create(
				ci_code = ci,
				test_code = row['test_code'],
				test_name = row['test_name'],
				scope_id = test_scope,
				tech_id = technology,
				inhouse_id = inhouse,
				eligibility = row['eligibility'],
				provided_id = provided,
				)

			# Populate target and essential/desirable target link tables
			for single_target in row['targets_essential']:
				
				hgnc = get_hgnc(single_target)

				target, created = TargetNov20.objects.get_or_create(
					target = single_target,
					hgnc_id = hgnc
					)

				link, created = EssentialTargetLinksNov20.objects.get_or_create(
					test_code = genomic_test,
					target_id = target,
					)


		elif directory_version == '2':
			# Populate cancer types table
			cancer_type, created = CancerTypeJul21.objects.get_or_create(
				cancer_type = row['cancer_type'],
			)

			# Populate test scopes table
			test_scope, created = ScopeJul21.objects.get_or_create(
				test_scope = row['test_scope'],
			)

			# Populate technologies table
			technology, created = TechnologyJul21.objects.get_or_create(
				technology = row['technology'],
			)

			# Populate in-house tests table
			inhouse, created = InHouseTestJul21.objects.get_or_create(
				inhouse = row['in_house_test'],
			)

			# Populate currently provided table
			provided, created = CurrentlyProvidedJul21.objects.get_or_create(
				provided = row['currently_provided'],
			)

			# Populate specialist table
			specialist_group, created = SpecialistJul21.objects.get_or_create(
				specialist_group = row['specialist_group'],
			)

			# Populate commissioning category table
			commissioning, created = CommissioningCategoryJul21.objects.get_or_create(
				commissioning = row['commissioning'],
			)

			# Populate family structure table
			family_structure, created = FamilyStructureJul21.objects.get_or_create(
				family_structure = row['family_structure'],
			)

			# Populate CITT comments table
			citt_comment, created = CITTJul21.objects.get_or_create(
				citt_comment = row['citt_comment'],
			)

			# Populate TT code table
			tt_code, created = TTJul21.objects.get_or_create(
				tt_code = row['tt_code'],
			)

			# Populate clinical indications table
			ci, created = ClinicalIndicationJul21.objects.get_or_create(
				cancer_id = cancer_type,
				ci_code = row['ci_code'],
				ci_name = row['ci_name'],
			)

			# Populate genomic tests table
			genomic_test, created = GenomicTestJul21.objects.get_or_create(
				ci_code = ci,
				test_code = row['test_code'],
				test_name = row['test_name'],
				specialist_id = specialist_group,
				scope_id = test_scope,
				tech_id = technology,
				inhouse_id = inhouse,
				cc_id = commissioning,
				eligibility = row['eligibility'],
				family_id = family_structure,
				provided_id = provided,
				citt_id = citt_comment,
				tt_id = tt_code,
				)

			# Populate target and essential/desirable target link tables
			target_fields = ['targets_essential', 'targets_desirable']

			for field in target_fields:
				for single_target in row[field]:

					hgnc = get_hgnc(single_target)

					target, created = TargetJul21.objects.get_or_create(
						target = single_target,
						hgnc_id = hgnc
						)

					if field == 'targets_essential':
						link, created = EssentialTargetLinksJul21.objects.get_or_create(
							test_code = genomic_test,
							target_id = target,
							)

					elif field == 'targets_desirable':
						link, created = DesirableTargetLinksJul21.objects.get_or_create(
							test_code = genomic_test,
							target_id = target,
							)


@limits(calls=10, period=1)
def get_hgnc(single_target):
	"""Get associated HGNC ID (where it exists) for each genomic test target.

	Args:
		target [string]: single target of a genomic test

	Returns:
		hgnc_id [string]: HGNC ID of target (if such exists)
	"""

	# Construct request to HGNC website REST using target symbol
	headers = {'Accept': 'application/json'}
	method = 'GET'
	body = ''
	h = http.Http()

	uri = 'http://rest.genenames.org'

	# Define a URL to search for the target in current gene symbols
	current_path = '/search/symbol/' + str(single_target)
	current_target = urlparse(uri + current_path)

	# Define a URL to search for the target in previous gene symbols
	previous_path = '/search/prev_symbol/' + str(single_target)
	previous_target = urlparse(uri + previous_path)

	# Make request to API with these URLs, look in current symbols first
	for target_url in [current_target, previous_target]:
		response, content = h.request(
			target_url.geturl(),
			method,
			body,
			headers
			)

		# If the request is successful, load json content
		if response['status'] == '200':
			data = json.loads(content)

			# If there is an HGNC ID value, the function returns this
			try:
				hgnc_id = str(data['response']['docs'][0]['hgnc_id'])
				return hgnc_id
			
			except IndexError:
				if target_url == current_target:
					continue

				else:
					return 'None'

		else:
			return 'None'
