#!usr/bin/env python

"""
Script to test the get_hgnc function defined in insert.py, using various
examples which should definitely or definitely not generate an HGNC ID
"""


import pandas as pd
from datetime import datetime


def initialise_output():

    # Get the current datetime and use this to name the output file
    check_time = str(datetime.now()) + '\n'

    # Initialise the output file
    with open('hgnc_test_output.txt', 'w') as file_object:
        file_object.write(check_time)


def specify_dump():

    # Specify the text file containing the HGNC website API dump
    hgnc_file = 'hgnc_dump_210727.txt'

    # Read this file into a pandas dataframe
    df = pd.read_csv(hgnc_file, sep='\t')

    return df


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


def main():

    initialise_output()
    df = specify_dump()

    # Targets which should have an HGNC ID
    have_id = [
        'A1BG',
        'KRAS',
        'NRAS',
        'EGFR',
        'ARAF',
        'ARID1A',
        'MAGI1',
        'SALL2',
        'GATA1',
        'H3C2',
        'HIST1H3B',
        ]

    # Targets which should NOT have an HGNC ID
    no_id = [
        'BCR-ABL',
        '1P19Q CODEL',
        '12P- & T(9;22)(Q34;Q11) BCR-ABL1',
        '-7/7QA1BG',
        'CHROMOSOME 3',
        'CRYPTIC DELETION OF 4Q12A1BG',
        'DEPENDENT ON CLINICAL INDICATION OR SPECIFIED REQUEST',
        'CALR EXON 9 HOTSPOT',
        'COMPLEX KARYOTYPE',
        'METHYLATION STATUS OF MULTIPLE CPG SITES',
        'COPY NUMBER CHANGES OF IKZF1',
        'NUP98 REARRANGEMENTS OTHER THAN NUP98-NSD1',
        'TERT PROMOTER',
        '11Q23 REARRANGEMENTS',
        'PAR1 REGION (CRLF2, CSF2RA, IL3RA)',
        'TRISOMY 12',
        'NPM1 TYPES A, B & D',
        'DEL(1)(P33P33)',
        'INV(3)',
        'I(17Q)',
        'T(1;7)(P32;Q11) TRB-TAL1',
        ]

    # For each target,
    for target_list in [have_id, no_id]:
        for target in target_list:

            # Run the function to get its HGNC ID
            hgnc = get_hgnc(df, target)

            # Construct an output sentence
            target_sentence = '\nTarget: {a} \n{b}\n'.format(a=target, b=hgnc,)

            # Write this sentence to the output file
            with open('hgnc_test_output.txt', 'a') as file_object:
                file_object.write(target_sentence)


if __name__ == '__main__':
    main()
