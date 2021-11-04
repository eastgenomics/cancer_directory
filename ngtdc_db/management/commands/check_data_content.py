#!usr/bin/env python

"""
Script to visualise what the get_data.py script is outputting for the
specified test directory version. Essentially does the same as seed.py, but
doesn't interact with insert.py or the database; just returns an output file
showing what values are in each field of get_data.py's output dataframe.

Useful for script testing before actually seeding the database.

Called from the command line with the command:

    python manage.py check_data_content -f <DIRECTORY VERSION>

The directory version supplied can currently be 1, 2, or 2D (for the
unofficial draft of the second directory version).
"""


import pandas as pd
from datetime import datetime

from django.core.management.base import BaseCommand
import ngtdc_db.management.commands.get_data as get_data
import ngtdc_db.management.commands.get_data_2D as get_data_2D


class Command(BaseCommand):
    help = "Seed the database"
    
    def add_arguments(self, parser):
        """Add 'file' argument for manage.py seed command."""

        parser.add_argument(
            "-f",
            "--file",
            help = 'The test directory version being used.',
			nargs = 1,
            )


    def initialise_output_file(self):
        """Initialise the text file which will contain the output."""

        # Get the current time
        check_time = str(datetime.now())

        # Construct an initial line for the output file
        initial_line = 'Data contents checked at: {a}'.format(a = check_time)

        # Create/overwrite a new file with the initial line
        with open('data_contents.txt', 'w') as file_object:
            file_object.write(initial_line)


    def check_df_dict(self, df_dict):
        """Optional check on each field of each dataframe:
        (a) total number of cells in field
        (b) number of unique cells in field
        (c) number of empty cells in field

        Within a cancer type:
        -all fields should have the same (a)
        -test_code should have (a)=(b), since it's unique for every row
        -ci_code and ci_name should have the same (b)
        -cancer_type should have (b)=1

        Args:
            df_dict: dictionary of pandas dfs containing NGTDC data
        """

        for df in df_dict:
            data = df_dict[df]
            print('\n{df}\n--------------------------'.format(df=df))

            exclude_fields = [
                'targets_essential',
                'targets_desirable',
                ]

            # print total, empty and unique cells
            for field in data.columns:
                if field not in exclude_fields:
                    column = data[field]
                    elements = str(len(column))
                    unique = str(len(column.unique()))
                    empty = str(column.isnull().sum())

                    print('{a} has length {b}, {c} are unique, {d} are empty'\
                        .format(a=field, b=elements, c=unique, d=empty))

                # or just print total and empty cells for targets fields
                else:
                    column = data[field]
                    elements = str(len(column))
                    empty = str(column.isnull().sum())

                    print('{a} has length {b}, {c} are empty'\
                        .format(a=field, b=elements, c=empty))


    def check_ci_test_codes(self, single_df):
        """
        Check that in each row, the prefix of the test code is the same as
        the CI code.
        """

        # Iterate over the dataframe's rows
        for index, row in single_df.iterrows():

            # Get the current row's CI code
            ci_code = row['ci_code']

            # Get the current row's test code
            test_code = row['test_code']

            # Get the prefix of the test code (should be same as CI code)
            test_code_prefix = test_code.split('.')[0]

            # If there is an issue,
            if ci_code != test_code_prefix:

                # Define an error message
                message =  '\nci/test code mismatch: {a} vs {b} at index {i}'.\
                    format(
                    a = ci_code,
                    b = test_code,
                    i=index,
                    )

                # Write this to the output text file
                with open('data_contents.txt', 'a') as file_object:
                    file_object.write(message)


    def output_field_info(self, single_df):
        """
        Print a list of unique elements for each field of the dataframe.
        """

        target_fields = ['targets_essential', 'targets_desirable']

        # Iterate over columns
        for field in single_df.columns:

            # Look at fields which don't contain targets first
            if field not in target_fields:

                # Get the number and values of unique elements in the column
                unique = single_df[field].unique()
                unique.sort()

                count = len(unique)

                # Construct a summary line for the column
                summary_line = (
                    '\n\n{a} has {b} unique values.\n\n'.format(
                        a = field,
                        b = count,
                        )
                    )

                # Write column information to the text file
                with open('data_contents.txt', 'a') as file_object:

                    # Start with the summary line
                    file_object.write(summary_line)

                    # Then print the list of unique values in that column
                    for element in unique:
                        line = '{a}\n'.format(a = element)
                        file_object.write(line)
            
            # Now look at columns which ARE lists of targets
            else:
                # Initialise an empty list to hold individual targets
                unique = []

                # Iterate over cells in the column
                for cell in single_df[field]:

                    # Iterate over cell (should be a list) elements
                    for element in cell:

                        # Add non-blank unique elements to the 'unique' list
                        if (element != '') and (element not in unique):
                            unique.append(element)
                
                # Get the number of unique elements
                count = len(unique)
                unique.sort()

                # Construct a summary line for the column
                summary_line = (
                    '\n\n{a} has {b} unique values.\n\n'.format(
                        a = field,
                        b = count,
                        )
                    )

                # Write column information to the output file
                with open('data_contents.txt', 'a') as file_object:

                    # Start with the summary line
                    file_object.write(summary_line)

                    # Then print a list of all unique elements
                    for element in unique:
                        line = '{a}\n'.format(a = element)
                        file_object.write(line)


    def clean_data(self, version):
        """Call get_data.py functions on the specified test directory version.

        Args:
            version: test directory version (1, 2 or 2D)
        
        Returns:
            single_df [pandas dataframe]: data from test directory .xlsx file
        
        """

        # Initialise variables to hold the input data
        xl_file = ''
        data = ''

        # Define the file and get_data script to use for version 1

        if version == '1':

            xl_file = (
                "National-Genomic-Test-Directory-Cancer-November-2020-21.xlsx"
                )
            data = get_data.Data(xl_file)
            print('Output for version 1 file:', xl_file)

        # Define the file and get_data script to use for version 2

        elif version == '2':

            xl_file = (
                "National-genomic-test-directory-cancer-October-2021-22-.xlsx"
                )
            data = get_data.Data(xl_file)
            print('Output for version 2 file:', xl_file)

        # Define the file and get_data script to use for the version 2 DRAFT

        elif version == '2D':

            xl_file = (
                "CONFIDENTIAL-Final-National-Genomic-"
                "Test-Directory-Cancer-20-21-v2_pstb.xlsx"
                )
            data = get_data_2D.Data(xl_file)
            print('Output for version 2 DRAFT:', xl_file)

        # Raise an error if any other version number is supplied
        else:
            raise ValueError('Specified directory version must be 1 or 2.')

        # Initialise the output file
        self.initialise_output_file()

        # Call the functions which apply to a dictionary of pandas dataframes
        df_dict_1 = data.get_xl_data(xl_file)
        df_dict_2 = data.rename_columns(df_dict_1)
        df_dict_3 = data.remove_blank_rows(df_dict_2)
        df_dict_4 = data.replace_merged_cells(df_dict_3)
        df_dict_5 = data.add_new_fields(df_dict_4)

        # Version 2 has an extra step
        if version == '2D':
            df_dict_6 = data.TEMPORARY_FIX_REPLACE_BLANK_TC(df_dict_5)
        
        elif (version == '1') or (version == '2'):
            df_dict_6 = df_dict_5

        # Run the multiple-dataframe check
        # self.check_df_dict(df_dict_6)

        # Call the functions which apply to a single consolidated dataframe
        single_df_1 = data.combine_dataframes(df_dict_6)
        single_df_2 = data.default_blank_values(single_df_1)
        single_df_3 = data.replace_newlines(single_df_2)
        single_df_4 = data.all_cells_to_strings(single_df_3)
        single_df_5 = data.targets_to_lists(single_df_4)

        # Run the single-dataframe check
        self.check_ci_test_codes(single_df_5)
        self.output_field_info(single_df_5)


    def handle(self, *args, **kwargs):
        """Check the contents of the dataframe generated by get_data.py"""

        # If there is a version supplied, use this as the 'version' variable
        if kwargs['file']:
            version = kwargs['file'][0]

            # Clean the data and produce output
            print('Cleaning data...')
            self.clean_data(version)
            print('Text file of output created.')

        # Otherwise don't do anything
        else:
            print('Directory version required in -f / --file argument.')
