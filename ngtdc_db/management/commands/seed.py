#!usr/bin/env python

"""
Calls the functions defined in get_data.py to extract and parse
information from an .xlsx file containing the data for a version of the
NGTDC. Passes the cleaned data to insert.py for insertion into the
Django SQLite database.

Called from the command line with the command:

    python manage.py seed -f <DIRECTORY VERSION>

The directory version supplied can currently be 1 or 2. This script does not
support version '2D' (the draft second version).
"""


import pandas as pd
from django.core.management.base import BaseCommand
import ngtdc_db.management.commands.get_data as get_data
import ngtdc_db.management.commands.insert as inserter


class Command(BaseCommand):
    help = "Call functions from get_data.py to import data from an .xlsx \
    test directory file, clean it, and insert it into the Django database."
    
    def add_arguments(self, parser):
        """
        Add 'file' argument for manage.py seed command, so that the
        test directory version can be supplied in the CL call.
        """

        parser.add_argument(
            "-f",
            "--file",
            help = 'The test directory version being used.',
			nargs = 1,
            )


    def clean_data(self, version):
        """
        Call the functions in get_data.py on the .xlsx file for the
        specified test directory version.

        Args:
            version [string]: test directory version ('1' or '2')
        
        Returns:
            single_df [pandas dataframe]: cleaned test directory data     
        """

        # Initialise variables to hold the input data
        xl_file = ''
        data = ''

        # Define the file and script to apply for version 1
        if version == '1':

            xl_file = (
                "National-Genomic-Test-Directory-Cancer-November-2020-21.xlsx"
                )
            data = get_data.Data(xl_file)
            print('Using file for version 1:', xl_file)

        # Define the file and script to apply for version 2
        elif version == '2':

            xl_file = (
                "National-genomic-test-directory-cancer-October-2021-22-.xlsx"
                )
            data = get_data.Data(xl_file)
            print('Using file for version 2:', xl_file)

        # Raise an error if any other version number is supplied
        else:
            raise ValueError('Version must be 1 or 2.')

        # Apply first set of functions from get_data.py
        #(Those which apply to a dictionary of dataframes)

        df_dict_1 = data.get_xl_data(xl_file)
        df_dict_2 = data.rename_columns(df_dict_1)
        df_dict_3 = data.remove_blank_rows(df_dict_2)
        df_dict_4 = data.replace_merged_cells(df_dict_3)
        df_dict_5 = data.add_new_fields(df_dict_4)

        # Apply second set of functions from get_data.py
        #(Those which apply to a single consolidated dataframe)

        single_df_1 = data.combine_dataframes(df_dict_5)
        single_df_2 = data.default_blank_values(single_df_1)
        single_df_3 = data.replace_newlines(single_df_2)
        single_df_4 = data.all_cells_to_strings(single_df_3)
        single_df_5 = data.targets_to_lists(single_df_4)

        return single_df_5


    def handle(self, *args, **kwargs):
        """
        Calls clean_data, then calls insert.py to insert the data into
        the Django database.
        """

        # If a version was specified in the CL command, this is 'version'
        
        if kwargs['file']:
            version = kwargs['file'][0]

            # Call clean_data to extract data from the .xlsx file and clean it

            print('Creating Pandas dataframe from Excel file.')
            cleaned_df = self.clean_data(version)
            print('Pandas dataframe created.\n')

            # Call insert.py to insert cleaned data into the Django database

            print('Populating Django database models...')
            inserter.insert_data(cleaned_df, version)
            print('Database population completed.')

        # If there isn't a version supplied, don't do anything
        else:
            print('Directory version required as -f / --file argument.')
