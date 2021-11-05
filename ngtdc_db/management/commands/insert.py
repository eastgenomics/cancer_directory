#!usr/bin/env python

"""
Called within seed.py. Looks through each row of the cleaned pandas
dataframe generated earlier in that script, and inserts each cell into the
relevant database model.

Args:
	cleaned_data [pandas dataframe]: generated earlier in the seed.py script
		which calls the insert_data function

	directory_version [string]: specified in the CL call to seed.py. Can
		currently be '1' or '2'.

Doesn't return anything, but updates the Django database.
"""

import pandas as pd
from django.contrib.auth.models import User

from ngtdc_db.models import (
	CancerType,
	ClinicalIndication,
	TestScope,
	Technology,
	Target,
	GenomicTest,
	EssentialTarget,
	)


def insert_data(cleaned_data, version):
	"""Insert data into the database"""
	
	# Specify the text file containing the HGNC website data dump
	hgnc_file = 'hgnc_dump_210727.txt'

	# Read this file into a pandas dataframe
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

			if version == '1':
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
						)
			
			elif version == '2':
				# Create GenomicTest table version 2 records
				genomic_test, created = GenomicTest.objects.\
					get_or_create(
						version = '2',
						ci_code = ci,
						test_code = row['test_code'],
						test_name = row['test_name'],
						scope_id = test_scope,
						tech_id = technology,
						currently_provided = row['currently_provided'],
						inhouse_technology = row['in_house_test'],
						eligibility = row['eligibility'],
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


def get_hgnc(df, single_target):
    """Get associated HGNC ID (where it exists) for each genomic test
	target, using tab-delimited .txt dump file sourced from HGNC website.

	Args:
		df [dataframe]: pandas dataframe of HGNC website data 
		single_target [string]: string value for single gene target

	Returns:
		hgnc_id [string]: target's HGNC ID if it exists, 'None' otherwise
	"""

	# If there is a row where the target is the official gene symbol,
    try:
		
		# Get that row's index
        target_index = df.index[df['symbol'] == single_target]

		# Retrieve the HGNC ID at that row index
        hgnc_id = df.loc[target_index[0], 'hgnc_id']

        return hgnc_id
    
	# If there is no row where the target is the official symbol, 
    except IndexError:

		# Create a sentry variable for whether an ID has been found yet
        has_id = False
        i = 0

		# Look through the 'previous official gene symbols' field
        for value in df['prev_symbol']:

			# If the target appears in a value in this column,
            if single_target in str(value):

				# The associated HGNC ID can be used for this target
                has_id = True

				# Retrieve and return the associated HGNC ID
                hgnc_id = df.iloc[i].loc['hgnc_id']

                return hgnc_id
            
            i += 1
        
		# If the target isn't either an official or previous gene symbol,
        if not has_id:

			# Set the HGNC ID value to 'None'
            return 'None'
