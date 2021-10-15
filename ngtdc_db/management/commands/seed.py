import pandas as pd
from django.core.management.base import BaseCommand
import ngtdc_db.management.commands.get_data_v1 as get_data_v1
import ngtdc_db.management.commands.get_data_v2 as get_data_v2
import ngtdc_db.management.commands.insert as inserter


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


    def clean_data(self, version):
        """Call the functions in get_data on the specified directory version.

        Args:
            version: test directory version (currently '1' or '2')
        
        Returns:
            single_df [pandas dataframe]: cleaned data from test directory file
            version [string]: string value of the version argument
        
        """

        # Initialise variables to hold the input data
        xl_file = ''
        data = ''

        # Define the file and get_data script to use for version 1
        if version == '1':

            xl_file = (
                "National-Genomic-Test-Directory-Cancer-November-2020-21.xlsx"
                )

            data = get_data_v1.Data(xl_file)
            print('Output for version 1 file:', xl_file)

        # Define the file and get_data script to use for version 2
        elif version == '2':

            xl_file = (
                "National-genomic-test-directory-cancer-October-2021-22-.xlsx"
                )

            data = get_data_v1.Data(xl_file)
            print('Output for version 2 file:', xl_file)

        # Define the file and get_data script to use for the DRAFT version 2 
        elif version == '2D':

            xl_file = (
                "CONFIDENTIAL-Final-National-Genomic-"
                "Test-Directory-Cancer-20-21-v2_pstb.xlsx"
                )

            data = get_data_v2.Data(xl_file)
            print('Output for version 2 DRAFT:', xl_file)

        # Raise an error if any other version number is supplied
        else:
            raise ValueError('Version must be 1, 2 or 2D (draft 2nd version).')

        # Functions which apply to a dictionary of pandas dataframes
        df_dict_1 = data.get_xl_data(xl_file)
        df_dict_2 = data.remove_blank_rows(df_dict_1)
        df_dict_3 = data.rename_columns(df_dict_2)
        df_dict_4 = data.replace_merged_cells(df_dict_3)
        df_dict_5 = data.default_blank_values(df_dict_4)
        df_dict_6 = data.replace_newlines(df_dict_5)
        df_dict_7 = data.add_new_fields(df_dict_6)

        # Version 2 requires another function to deal with missing test codes
        if version == '2D':
            df_dict_8 = data.TEMPORARY_FIX_REPLACE_BLANK_TC(df_dict_7)
        
        elif version == ('1' or '2'):
            df_dict_8 = df_dict_7

        # Functions which apply to a single consolidated dataframe
        single_df_1 = data.combine_dataframes(df_dict_8)
        single_df_2 = data.all_cells_to_strings(single_df_1)
        single_df_3 = data.targets_to_lists(single_df_2)

        return single_df_3


    def handle(self, *args, **kwargs):
        """Gets data from .xlsx file and inserts into Django database."""

        # If there is a version supplied, use this as the 'version' variable
        if kwargs['file']:
            version = kwargs['file']

            # Apply the clean_data function
            print('Creating Pandas dataframe from Excel file.')
            cleaned_df = self.clean_data(version[0])
            print('Pandas dataframe created.\n')

            # Insert cleaned data into the Django database
            print('Populating Django database models...')
            inserter.insert_data(cleaned_df, version)
            print('Database population completed.')

        # If there isn't a version supplied, don't do anything
        else:
            print('Directory version required as -f / --file argument.')
