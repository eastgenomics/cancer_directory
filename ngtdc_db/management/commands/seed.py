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


    def clean_data(self, file_version):
        """Call get_data.py functions on the specified test directory
        version.

        Args:
            version: test directory version (1 or 2)
        
        Returns:
            single_df [pandas dataframe]: data from test directory file
        
        """

        xl_file = ''
        data = ''

        # Specify the file and script to use for seeding with version 1 data
        if file_version == '1':

            xl_file = (
                "National-Genomic-Test-Directory-"
                "Cancer-November-2020-21.xlsx"
                )

            data = get_data_v1.Data(xl_file)
            print('Seeding with version 1 file:', xl_file)

        # Specify the file and script to use for seeding with version 2 data
        elif file_version == '2':

            xl_file = (
                "CONFIDENTIAL-Final-National-Genomic-"
                "Test-Directory-Cancer-20-21-v2_pstb.xlsx"
                )
            
            data = get_data_v2.Data(xl_file)
            print('Seeding with version 2 file:', xl_file)
        
        else:
            raise ValueError('Specified directory version must be 1 or 2.')

        # Functions which apply to a dictionary of pandas dataframes
        df_dict_1 = data.get_xl_data(xl_file)
        df_dict_2 = data.remove_blank_rows(df_dict_1)
        df_dict_3 = data.rename_columns(df_dict_2)
        df_dict_4 = data.replace_merged_cells(df_dict_3)
        df_dict_5 = data.default_blank_values(df_dict_4)
        df_dict_6 = data.add_new_fields(df_dict_5)

        if file_version == '2':
            df_dict_7 = data.TEMPORARY_FIX_REPLACE_BLANK_TC(df_dict_6)
        
        elif file_version == '1':
            df_dict_7 = df_dict_6

        # Functions which apply to a single consolidated dataframe
        single_df_1 = data.combine_dataframes(df_dict_7)
        single_df_2 = data.all_cells_to_strings(single_df_1)
        single_df_3 = data.targets_to_lists(single_df_2)

        return single_df_3, file_version


    def handle(self, *args, **kwargs):
        """Gets data from .xlsx file and inserts into Django database."""

        # Requires a filepath to be provided
        if kwargs['file']:
            version = kwargs['file']

            # Applies functions in get_data.py script to provided .xlsx file
            cleaned_df, version = self.clean_data(version[0])
            print('Pandas dataframe created from Excel file.')
            print('Populating Django database models...')

            # Inserts data into Django database
            inserter.insert_data(cleaned_df, version)
            print('Database population completed.')
        
        else:
            print('Directory version required in -v / --version argument.')
