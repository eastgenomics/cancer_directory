import pandas as pd

from django.core.management.base import BaseCommand

import ngtdc_db.management.commands.get_data as get_data
import ngtdc_db.management.commands.insert as inserter


class Command(BaseCommand):
    help = "Seed the database"
    
    # Enable passing data in a file as an argument for the seed command
    def add_arguments(self, parser):
        parser.add_argument("-f", "--filepath", help = 'The path to the data',
			nargs = 1)
    

    # Call the functions in get_data.py on the specified file
    def clean_data(self, filepath):
        print(filepath)

        data = get_data.Data(filepath)
        
        df_dict = data.get_xl_data(filepath)
        data.remove_blank_rows(df_dict)
        data.replace_merged_cells(df_dict)
        data.rename_columns(df_dict)
        data.sheetname_as_field(df_dict)

        single_df = data.combine_dataframes(df_dict)
        data.all_cells_to_strings(single_df)
        data.targets_to_lists(single_df)
        # data.scopes_to_lists(single_df)
        # data.tech_to_lists(single_df)

        print('seed.py Command.clean_data function completed')

        return single_df
    

    # If a filepath is provided, clean the data and insert it into the database
    def handle(self, *args, **kwargs):
        if kwargs['filepath']:
            filepath = kwargs['filepath']

            cleaned_df = self.clean_data(filepath[0])
            inserter.insert_data(cleaned_df)
        
        print('seed.py Command.handle function completed')
