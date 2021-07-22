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
        """Call get_data.py functions on the specified test directory version.

        Args:
            version: test directory version (1 or 2)
        
        Returns:
            single_df [pandas dataframe]: data from test directory .xlsx file
        
        """

        xl_file = ''
        data = ''

        if file_version == '1':
            xl_file = """National-Genomic-Test-Directory-Cancer-November-2020-21.xlsx"""

            data = get_data_v1.Data(xl_file)
            print('Seeding with version 1 file:', xl_file)
        
        elif file_version == '2':
            xl_file = """CONFIDENTIAL-Final-National-Genomic-Test-Directory-Cancer-20-21-v2_pstb.xlsx"""

            data = get_data_v2.Data(xl_file)
            print('Seeding with version 2 file:', xl_file)
        
        else:
            raise ValueError('Specified directory version must be 1 or 2.')

        # Functions which apply to a dictionary of pandas dataframes
        df_dict = data.get_xl_data(xl_file)
        data.remove_blank_rows(df_dict)
        data.rename_columns(df_dict)
        data.replace_merged_cells(df_dict)
        data.default_blank_values(df_dict)
        data.add_new_fields(df_dict)

        if file_version == '2':
            data.TEMPORARY_FIX_BLANK_TCS(df_dict)

        # Functions which apply to a single consolidated dataframe
        single_df = data.combine_dataframes(df_dict)
        data.all_cells_to_strings(single_df)
        data.targets_to_lists(single_df)

        return single_df, file_version
    

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
