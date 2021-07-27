import pandas as pd
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


def insert_data(cleaned_data, directory_version):
	"""Insert data into the database"""
	
	# File containing data from HGNC website
	hgnc_file = 'hgnc_dump_210727.txt'
	df = pd.read_csv(hgnc_file, sep='\t')

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
				
				hgnc = get_hgnc(df, single_target)

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

					hgnc = get_hgnc(df, single_target)

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


def get_hgnc(df, single_target):
    """Get associated HGNC ID (where it exists) for each genomic test target.
    Gets HGNC IDs from tab-delimited .txt file sourced from HGNC website.

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
