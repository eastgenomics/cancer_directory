#!usr/bin/env python

"""

THIS SCRIPT SPECIFICALLY APPLIES TO THE DRAFT FORM OF VERSION 2

National Genomic Test Directory for Cancer (NGTDC)

This script defines functions to access the National Genomic Test 
Directory for Cancer (in the form of a downloaded MS Excel file), 
convert its worksheets into a dictionary of pandas dataframes, combine
them into a single dataframe, and format the data for subsequent
insertion into a database. The script is accessed by the seed.py
script.

Functions:
    Get data as a dictionary of pandas dataframes
    Remove any completely blank rows
    Rename columns to be more programming-friendly
    Replace NaN values caused by merged cells in the original file
    TEMPORARY fix for rows with blank test code
    Add additional requested fields
    Combine worksheets into a single dataframe
    Replace any newline characters with spaces
    Set default values for blank cells
    Convert all cells into strings and remove excess whitespace
    Convert cells in the 'targets' column into lists of targets

Inputs:
    filepath: path to an .xlsx file containing data for the draft second
        version of the NGTDC

Returns:
    single_df [pandas dataframe]: data converted into a dataframe

"""


import pandas as pd


class Data:
    def __init__(self, filepath):
        self.filepath = filepath


    def get_xl_data(self, filepath):
        """
        Accesses an .xlsx file containing data for the draft second
        version of the NGTDC, and converts each worksheet into a pandas
        dataframe. Creates a dictionary of these dataframes named
        df_dict.

        Args:
            filepath: path to .xlsx file containing NGTDC data

        Returns:
            df_dict [dict]: dictionary of pandas DataFrames
                keys: worksheet name e.g. 'Sarcomas'
                values: dataframe of columns A-H from relevant worksheet
        """

        # Specify which worksheets to read in
        sheets = [
            'Solid Tumours (2)',
            'Neurological tumours (2)',
            'Sarcoma (2)',
            'Haematological (2)',
            'Paediatric (2)',
            ]

        # Create pandas object with dfs as columns A-P of each worksheet
        df_dict = pd.read_excel(
            filepath,
            sheets,
            usecols='B:P',
            )

        return df_dict


    def rename_columns(self, df_dict):
        """
        Renames the columns to make them more programming-friendly
        (i.e. no spaces or parentheses).

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: columns have been renamed in each df
        """

        # Create list of new column names
        renamed_columns = [
            'cancer_type',
            'specialist_group',
            'ci_code',
            'ci_name',
            'test_code',
            'test_name',
            'targets_essential',
            'targets_desirable',
            'test_scope',
            'technology',
            'family_structure',
            'commissioning',
            'eligibility',
            'citt_comment',
            'tt_code',
            ]

        for df in df_dict:
            data = df_dict[df]
            
            # Rename dataframe columns
            data.columns = renamed_columns

        return df_dict


    def remove_blank_rows(self, df_dict):
        """
        Removes any rows where all cells have NaN values.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: blank rows have been removed from each df
        """

        for df in df_dict:
            data = df_dict[df]

            # Remove rows where all cells are blank
            data.dropna(axis=0,
            how='all',
            inplace=True,
            )

            # Reset row index to be a consistent series
            data.index = range(len(data))

        return df_dict


    def replace_merged_cells(self, df_dict):
        """
        Columns B-E (tumour group, specialist test group, CI code and
        name) contain merged cells, which translate to 'NaN' values in
        df_dict. This function replaces the NaN values from merged cells
        with the appropriate value.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: cells which were merged in the xlsx now have values
        """

        for df in df_dict:
            data = df_dict[df]

            i = 0
            for row in data.iterrows():

                # if cell was merged in the xls worksheet,
                if pd.isna(row[1]['ci_code']):

                    # update cell value to that of the cell above it
                    data.loc[i, 'ci_code'] = data.loc[i-1, 'ci_code']

                    # similarly update adjacent cells in cols B, C, E
                    data.loc[i, 'cancer_type'] = data.loc[i-1, 'cancer_type']

                    data.loc[i, 'specialist_group'] = data.loc[i-1,
                        'specialist_group']

                    data.loc[i, 'ci_name'] = data.loc[i-1, 'ci_name']

                i += 1

        return df_dict


    def add_new_fields(self, df_dict):
        """
        Creates 2 additional fields for each row in each df:

        -in_house_test: currently 'Not specified' for all tests
        -currently_provided: currently 'Not specified' for all tests

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: new fields have been added to each dataframe
        """

        for df in df_dict:
            data = df_dict[df]

            default_value = 'Not specified'

            # Create new fields and set default values for every cell
            data['in_house_test'] = default_value
            data['currently_provided'] = default_value

        return df_dict


    def TEMPORARY_FIX_REMOVE_BLANK_TC(self, df_dict):
        """
        Because test_code is the primary key for the GenomicTest model,
        all records must have a unique value for this field. Version 2 of
        the test directory is problematic because many records have a blank
        test code value, meaning they all get assigned a non-unique value of
        'Not specified' (thanks version 2).
        
        There is also an issue where two different tests have been assigned
        the test code 'M150.6'. 
        
        This function removes any records where the test code is blank, as
        well as the two tests with the same test code.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: removes rows with test code = 'Not specified'
        """

        for df in df_dict:
            data = df_dict[df]

            # If a row has a test code value of 'Not specified', drop the row
            data.drop(
                data.loc[data['test_code']=='Not specified'].index,
                inplace=True,
                )

            # If a row has a test code value of 'M150.6', drop the row
            data.drop(
                data.loc[data['test_code']=='M150.6'].index,
                inplace=True,
                )

            # Reset row index to be a consistent series
            data = data.reset_index

        return df_dict


    def TEMPORARY_FIX_REPLACE_BLANK_TC(self, df_dict):
        """
        Because test_code is the primary key for the GenomicTest model,
        all records must have a unique value for this field. Version 2 of
        the test directory is problematic because many records have a blank
        test code value, meaning they all get assigned a non-unique value of
        'Not specified' (thanks version 2).
        
        There is also an issue where two different tests have been assigned
        the test code 'M150.6'. 
        
        This function replaces any blank test code values with a temporary
        identifier. The two tests with the same test code of M150.6 are
        removed to avoid confusion.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: rows with test code = 'Not specified' removed
        """

        for df in df_dict:
            data = df_dict[df]

            i = 0
            for index, row in data.iterrows():

                # If a test code is blank:
                if row['test_code'] == 'Not specified':

                    # If the row above it doesn't have a temporary identifier,
                    # this is the first temporary test code for that CI
                    if 'temp' not in data.iloc[i-1].loc['test_code']:
                        x = 1

                    # If the row above it DOES have a temporary identifer,
                    # increment the temporary identifier number
                    elif 'temp' in data.iloc[i-1].loc['test_code']:
                        x += 1

                    # Define a temporary identifier based on the CI and the
                    # incrementing number
                    temp_tc = '{ci}.temp_{x}'.format(
                        ci=row['ci_code'],
                        x=x
                        )

                    # Replace the empty test_code field with this value
                    data.iloc[i].loc['test_code'] = temp_tc
                    data.iloc[i].loc['test_name'] = 'No test code assigned'

                i += 1

            # If a row has a test code value of 'M150.6', drop the row
            data.drop(
                data.loc[data['test_code']=='M150.6'].index,
                inplace=True,
                )

            # Reset the row index to be a consistent series
            data = data.reset_index

        return df_dict


    def combine_dataframes(self, df_dict):
        """
        Combines all of the dfs in df_dict into a single dataframe.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            single_df [pandas df]: a single df, created by concatenating all
                the dfs in df_dict
        """

        # Combine all dataframes from df_dict into one
        single_df = pd.concat(
            df_dict,
            ignore_index = True,
            keys = df_dict.keys(),
            )

        return single_df


    def default_blank_values(self, single_df):
        """Set the value of all empty cells to be 'Not specified'.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: blank cells replaced with default value
        """

        # Define the default value for blank cells
        blank_value = 'Not specified'

        # Set all empty cells to have the default value
        single_df.fillna(blank_value, inplace=True)

        # Also set cells to the default value if they strip to an empty string
        single_df = single_df.applymap(
            lambda x: 'Not specified' if str(x).strip() == '' else x
        )

        return single_df


    def replace_newlines(self, single_df):
        """
        All newline characters in any cell are replaced with spaces
        because they mess up formatting.

        Args:
            single_df [pandas df]: dataframe containing NGTDC data

        Returns:
            single_df [pandas df]: newline characters are replaced with spaces
        """

        # Replace all newline characters in any dataframe cell with spaces
        single_df = single_df.applymap(lambda x: x.replace('\n', ' '))

        return single_df


    def all_cells_to_strings(self, single_df):
        """
        Converts all cells into strings and strips excess whitespace.

        Args:
            single_df [pandas df]: dataframe containing NGTDC data

        Returns:
            single_df [pandas df]: all cells changed to stripped strings
        """

        # convert every cell value to a string, and strip whitespace
        single_df = single_df.applymap(lambda x: str(x).strip())

        return single_df


    """
    Each cell in the targets column is currently a string, and needs to be
    converted into a list. Each list element will be a string representing a
    single target from that cell.

    e.g. 'NTRK1, NTRK2, NTRK3' becomes ['NTRK1', 'NTRK2', 'NTRK3']

    Text is converted to uppercase to avoid duplication issues 
    (e.g. '1q2' vs. '1Q2').

    There are some target cells which are dealt with in separate functions:
        -Cells with the value 'Not specified'
        -Cells containing sublists
    
    Args:
        single_df [pandas df]: dataframe containing NGTDC data

    Returns:
        single_df [pandas df]: cells in the targets column are
            converted from a string to a list of strings
    """


    def target_lists_notspecified(self, single_df):
        """
        Deals with cells in the targets column which have the value 
        'Not specified'; converts them to a single-element list.
        """

        # Define the new value to be used
        new_value = ['Not specified', ]

        # Define which fields to look at
        fields = ['targets_essential', 'targets_desirable']

        # Iterate over these fields in each row
        for index, row in single_df.iterrows():
            for field in fields:
                cell = row[field]

                # If a cell's value is 'Not specified', replace it
                if cell == 'Not specified':
                    single_df.loc[index, field] = new_value

        return single_df


    def target_lists_sublists(self, single_df):
        """
        Deals with cells in the targets column which have awkward commas;
        converts them to a single-element list.
        """

        # Define which fields to look at
        fields = ['targets_essential', 'targets_desirable']

        # Iterate over these fields in each row
        for index, row in single_df.iterrows():
            for field in fields:

                # Ignore any cells which are already lists of targets
                if type(row[field]) == list:
                    continue

                # Define the current cell, convert to uppercase
                cell = row[field]
                uppercase = str(cell).upper()

                # If the cell is an awkward case...
                # (Note: must be 'types' not 'type' to exclude 'karyotype')

                if ('TRANSCRIPTS' in uppercase) or \
                    ('TYPES' in uppercase) or \
                    (uppercase == '1P, 3, 6, 8'):

                    # Make the cell's value the sole element of a new list
                    new_value = [uppercase, ]

                    # Replace the original string value with this value
                    single_df.loc[index, field] = new_value

        return single_df


    def target_lists_other(self, single_df):
        """
        The main function for converting target cell strings to lists. There
        are still several awkward cases which need cleaning, like cells
        containing the PAR1 region, those with unnecessary text, or those
        with inappropriate brackets.

        There is a lot to do here, so this function is a bit of a monster.
        """

        # Define which fields to look at
        fields = ['targets_essential', 'targets_desirable']

        # Look at these fields over each row of the database
        for index, row in single_df.iterrows():
            for field in fields:

                # Ignore any cells which are already lists of targets
                if type(row[field]) == list:
                    continue

                # Define the current cell being looked at, convert to uppercase
                cell = row[field]
                uppercase = str(cell).upper()

                # Initialise an empty list to be the cell's new value
                new_value = []

                # If the cell contains the PAR1 region (awkward because it has
                # a sublist), extract this substring to be the first element of
                # the new list. Then deal with the cell remainder separately.

                par1_region = 'PAR1 REGION (CRLF2, CSF2RA, IL3RA)'

                if par1_region in uppercase:                
                    new_value.append(par1_region)
                    old_cell_string = uppercase.replace(par1_region, '')

                else:
                    old_cell_string = uppercase

                # old_cell_string is a string that may need more cleaning.
                # to_split is the string that will be split into a list.

                # Some cells contain unnecessary text
                text_to_remove = [
                    'TO INCLUDE DETECTION OF',
                    'TO INCLUDE:',
                    'TO INCLUDE',
                    'E.G.',
                    ]

                # If the cell contains one of these substrings, remove it
                for extra_text in text_to_remove:
                    if extra_text in old_cell_string:
                        to_split = old_cell_string.replace(extra_text, '')

                    else:
                        to_split = old_cell_string

                # Split the cleaned string into a list on a comma delimiter

                old_cell_list = to_split.split(',')

                # Now go through and clean each element of this new list 

                for element in old_cell_list:

                    # Strip excess whitespace from each element
                    stripped = element.strip()

                    # Ignore any elements which are empty strings
                    if stripped == '':
                        continue

                    # Get rid of any unnecessary brackets in each element:
                    # If the string is fully contained in brackets,

                    elif ((stripped[0] == '(') and (stripped[-1] == ')'))\
                            or \
                        ((stripped[0] == '[') and (stripped[-1] == ']')):

                        target = stripped[1:-1]
                        new_value.append(target)

                    # If the string starts with an unpaired bracket,

                    elif ((stripped[0] == '[') and (']' not in stripped))\
                            or \
                        ((stripped[0] == '(') and (')' not in stripped)):

                        target = stripped[1:]
                        new_value.append(target)

                    # Or if the string ends with an unpaired bracket.

                    elif ((stripped[-1] == ']') and ('[' not in stripped))\
                            or \
                        ((stripped[-1] == ')') and ('(' not in stripped)):

                        target = stripped[:-1]
                        new_value.append(target)

                    # Otherwise just append to cell's new list

                    else:
                        target = stripped
                        new_value.append(target)

                # Replace cell's old string value with new_value list
                single_df.loc[index, field] = new_value

        return single_df


    def UNUSED_scopes_to_lists(self, single_df):
        """Iterates over column 5 (test_scope) and changes each cell to a
        list, each element of which is a string representing a single scope
        of the test. If a cell is empty, it is changed to a single-element
        list. 

        Args:
            single_df [pandas df]: contains NGTDC data

        Returns:
            single_df [pandas df]: cells in column 5 are now lists
        """

        i = 0
        for row in single_df.iterrows():
            scope = row[1]['test_scope']
            new_cell = []

            if pd.isna(scope):
                new_cell.append('Not specified')
            
            elif '/' in scope:
                scope_list = scope.split('/')
                stripped = [element.strip() for element in scope_list]

                for single_scope in stripped:
                    new_cell.append(single_scope)
            
            elif ';' in scope:
                scope_list = scope.split(';')
                stripped = [element.strip() for element in scope_list]

                for single_scope in stripped:
                    new_cell.append(single_scope)
            
            else:
                stripped = scope.strip()
                new_cell.append(stripped)
            
            single_df.loc[i, 'test_scope'] = new_cell
            i += 1

        return single_df


    def UNUSED_tech_to_lists(self, single_df):
        """Iterates over column 6 (technology) and changes each cell to a
        list, each element of which is a string representing a single
        technology. If a cell is empty, it is changed to a single-element
        list. 

        Args:
            single_df [pandas df]: contains NGTDC data

        Returns:
            single_df [pandas df]: cells in column 6 are now lists
        """

        i = 0
        for row in single_df.iterrows():
            technology = row[1]['technology']
            new_cell = []

            if pd.isna(technology):
                new_cell.append('Not specified')
            
            elif '/' in technology:
                tech_list = technology.split('/')
                stripped = [element.strip() for element in tech_list]

                for tech in stripped:
                    new_cell.append(tech)
            
            elif ';' in technology:
                tech_list = technology.split(';')
                stripped = [element.strip() for element in tech_list]
                
                for tech in stripped:
                    new_cell.append(tech)
            
            else:
                stripped = technology.strip()
                new_cell.append(stripped)
            
            single_df.loc[i, 'technology'] = new_cell
            i += 1

        return single_df
