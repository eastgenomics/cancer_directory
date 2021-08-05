import pandas as pd
from django.contrib.auth.models import User

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


def insert_data(cleaned_data, directory_version):
	"""Insert data into the database"""
	
	# File containing data from HGNC website
	hgnc_file = 'hgnc_dump_210727.txt'
	df = pd.read_csv(hgnc_file, sep='\t')

	for index, row in cleaned_data.iterrows():

			# Populate cancer types table
			cancer_type, created = CancerType.objects.get_or_create(
				cancer_type = row['cancer_type'],
				)

			# Populate clinical indications table
			ci, created = ClinicalIndication.objects.get_or_create(
				cancer_id = cancer_type,
				ci_code = row['ci_code'],
				ci_name = row['ci_name'],
				)

			# Populate test scopes table
			test_scope, created = TestScope.objects.get_or_create(
				test_scope = row['test_scope'],
				)

			# Populate technologies table
			technology, created = Technology.objects.get_or_create(
				technology = row['technology'],
				)

			if directory_version == '1':

				# The specialist_test_group, commissioning_category,
				# optimal_family_structure, and citt_comment fields do not
				# exist in directory version 1

				specialist_test_group, created = SpecialistTestGroup.objects.\
					get_or_create(
						specialist_test_group = '-',
						)

				commissioning, created = CommissioningCategory.objects.\
					get_or_create(
						commissioning = '-',
						)

				family_structure, created = OptimalFamilyStructure.objects.\
					get_or_create(
						family_structure = '-',
						)

				citt_comment, created = CITTComment.objects.get_or_create(
					citt_comment = '-',
					)

				genomic_test, created = GenomicTest.objects.\
					get_or_create(
						version = '1',
						ci_code = ci,
						test_code = row['test_code'],
						test_name = row['test_name'],
						scope_id = test_scope,
						tech_id = technology,
						currently_provided = row['currently_provided'],
						inhouse_technology = row['in_house_test'],
						eligibility = row['eligibility'],
						specialist_id = specialist_test_group,
						cc_id = commissioning,
						family_id = family_structure,
						citt_id = citt_comment,
						tt_code = '-',
						)

			elif directory_version == '2':

				# Populate specialist table
				specialist_test_group, created = SpecialistTestGroup.objects.\
					get_or_create(
						specialist_test_group = row['specialist_group'],
						)

				# Populate commissioning category table
				commissioning, created = CommissioningCategory.objects.\
					get_or_create(
						commissioning = row['commissioning'],
						)

				# Populate family structure table
				family_structure, created = OptimalFamilyStructure.objects.\
					get_or_create(
						family_structure = row['family_structure'],
						)

				# Populate CITT comments table
				citt_comment, created = CITTComment.objects.get_or_create(
					citt_comment = row['citt_comment'],
					)

				# Populate genomic tests table
				genomic_test, created = GenomicTest.objects.get_or_create(
					version = '2',
					ci_code = ci,
					test_code = row['test_code'],
					test_name = row['test_name'],
					specialist_id = specialist_test_group,
					scope_id = test_scope,
					tech_id = technology,
					currently_provided = row['currently_provided'],
					inhouse_technology = row['in_house_test'],
					cc_id = commissioning,
					eligibility = row['eligibility'],
					family_id = family_structure,
					citt_id = citt_comment,
					tt_code = row['tt_code'],
					)

			# Populate target and essential/desirable target link tables
			for single_target in row['targets_essential']:

				hgnc = get_hgnc(df, single_target)

				target, created = Target.objects.get_or_create(
					target = single_target,
					hgnc_id = hgnc
					)

				essential_link, created = EssentialTarget.objects.\
					get_or_create(
						test_id = genomic_test,
						target_id = target,
						)

			if directory_version == '2':
				for single_target in row['targets_desirable']:
					hgnc = get_hgnc(df, single_target)

					target, created = Target.objects.get_or_create(
						target = single_target,
						hgnc_id = hgnc
						)

					desirable_link, created = DesirableTarget.objects.\
						get_or_create(
							test_id = genomic_test,
							target_id = target,
							)


def get_hgnc(df, single_target):
    """Get associated HGNC ID (where it exists) for each genomic test
	target. Gets HGNC IDs from tab-delimited .txt file sourced from HGNC
	website.

	Args:
		df [dataframe]: pandas dataframe of HGNC website data 
		single_target [string]: single target of a genomic test

	Returns:
		hgnc_id [string]: target's HGNC ID if it exists, 'None' otherwise
	"""

    try:
		# Look for the target in the column of official gene symbols
        target_index = df.index[df['symbol'] == single_target]

		# Get the associated HGNC ID
        hgnc_id = df.loc[target_index[0], 'hgnc_id']

        return hgnc_id
    
    except IndexError:
        has_id = False
        i = 0

		# Look through the column of previous official gene symbols
        for value in df['prev_symbol']:

			# If the target appears in a value in this column,
            if single_target in str(value):
                has_id = True

				# Get the associated HGNC ID
                hgnc_id = df.iloc[i].loc['hgnc_id']

                return hgnc_id
            
            i += 1
        
		# If the target doesn't appear in the HGNC data its value is 'None'
        if not has_id:
            return 'None'
