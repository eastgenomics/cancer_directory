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
	
	# Tab-separated file containing HGNC data
	hgnc_file = 'hgnc_dump_210727.txt'

	# Read this file into a dataframe
	df = pd.read_csv(hgnc_file, sep='\t')

	for index, row in cleaned_data.iterrows():

			# Create CancerType table records
			cancer_type, created = CancerType.objects.get_or_create(
				cancer_type = row['cancer_type'],
				)

			# Create ClinicalIndication table records
			ci, created = ClinicalIndication.objects.get_or_create(
				cancer_id = cancer_type,
				ci_code = row['ci_code'],
				ci_name = row['ci_name'],
				)

			# Create TestScope table records
			test_scope, created = TestScope.objects.get_or_create(
				test_scope = row['test_scope'],
				)

			# Create Technology table records
			technology, created = Technology.objects.get_or_create(
				technology = row['technology'],
				)

			if directory_version == '1':

				# The specialist_test_group, commissioning_category,
				# optimal_family_structure, and citt_comment fields do not
				# exist in directory version 1; so create a record of '-' for
				# each of them

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

				# Create GenomicTest table version 1 records
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

				# Create SpecialistTestGroup table records
				specialist_test_group, created = SpecialistTestGroup.objects.\
					get_or_create(
						specialist_test_group = row['specialist_group'],
						)

				# Create CommissioningCategory table records
				commissioning, created = CommissioningCategory.objects.\
					get_or_create(
						commissioning = row['commissioning'],
						)

				# Create OptimalFamilyStructure table records
				family_structure, created = OptimalFamilyStructure.objects.\
					get_or_create(
						family_structure = row['family_structure'],
						)

				# Create CITTComment table records
				citt_comment, created = CITTComment.objects.get_or_create(
					citt_comment = row['citt_comment'],
					)

				# Create GenomicTest table version 2 records
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

			# Iterate over individual targets in 'targets_essential' cell
			for single_target in row['targets_essential']:

				# Get the HGNC ID if it exists
				hgnc = get_hgnc(df, single_target)

				# Create Target table records
				target, created = Target.objects.get_or_create(
					target = single_target,
					hgnc_id = hgnc,
					)

				# Create EssentialTarget table records
				essential_link, created = EssentialTarget.objects.\
					get_or_create(
						test_id = genomic_test,
						target_id = target,
						)

			# Do the same for desirable targets, but only for directory
			# version 2 (version 1 doesn't have this field)

			if directory_version == '2':
				for single_target in row['targets_desirable']:

					hgnc = get_hgnc(df, single_target)

					target, created = Target.objects.get_or_create(
						target = single_target,
						hgnc_id = hgnc,
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
		# Get the row index where the supplied target is the official gene
		# symbol (if such a row exists)
        target_index = df.index[df['symbol'] == single_target]

		# Retrieve the HGNC ID from that row index
        hgnc_id = df.loc[target_index[0], 'hgnc_id']

        return hgnc_id
    
	# If there is no row where the target is the official symbol, 
    except IndexError:
        has_id = False
        i = 0

		# Look in the field for previous official gene symbols instead
        for value in df['prev_symbol']:

			# If the target appears in a value in this column,
            if single_target in str(value):
                has_id = True

				# Retrieve the associated HGNC ID
                hgnc_id = df.iloc[i].loc['hgnc_id']

                return hgnc_id
            
            i += 1
        
		# If the target doesn't appear as either an official or previous gene
		# symbol, its HGNC ID value is 'None'
        if not has_id:
            return 'None'
