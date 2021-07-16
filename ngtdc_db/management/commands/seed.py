import pandas as pd
from django.core.management.base import BaseCommand
import ngtdc_db.management.commands.get_data as get_data
import ngtdc_db.management.commands.insert as inserter


class Command(BaseCommand):
    help = "Seed the database"
    
    def add_arguments(self, parser):
        """Add 'filepath' argument for manage.py seed command."""

        parser.add_argument(
            "-f",
            "--filepath",
            help = 'The path to the data. Should be .xlsx file format.',
			nargs = 1,
            )


    def clean_data(self, filepath):
        """Call get_data.py functions on the specified filepath.

        Args:
            filepath: path to .xlsx file containing test directory data
        
        Returns:
            single_df [pandas dataframe]: contains data used to populate Django
            database
        
        """

        print(filepath)
        data = get_data.Data(filepath)

        # Functions which apply to a dictionary of pandas dataframes
        df_dict = data.get_xl_data(filepath)
        data.remove_blank_rows(df_dict)
        data.replace_merged_cells(df_dict)
        data.rename_columns(df_dict)
        data.add_new_fields(df_dict)

        # Functions which apply to a single consolidated dataframe
        single_df = data.combine_dataframes(df_dict)
        data.all_cells_to_strings(single_df)
        data.targets_to_lists(single_df)

        return single_df
    

    def handle(self, *args, **kwargs):
        """Gets data from .xlsx file and inserts into Django database."""

        # Requires a filepath to be provided
        if kwargs['filepath']:
            filepath = kwargs['filepath']

            # Applies functions in get_data.py script to provided .xlsx file
            cleaned_df = self.clean_data(filepath[0])

            print(
                'Pandas dataframe created from Excel file.'\
                'Creating records in database models.'
                )

            # Inserts data into Django database
            inserter.insert_data(cleaned_df)

            print('Database population completed.')
        
        else:
            print('Please supply path to file as -f or --filepath argument')
