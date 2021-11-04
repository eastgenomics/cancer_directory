#!usr/bin/env python

"""

National Genomic Test Directory for Cancer (NGTDC)

This script defines functions to access the National Genomic Test 
Directory for Cancer (in the form of a downloaded MS Excel file), 
convert its worksheets into a dictionary of pandas dataframes, combine
them into a single dataframe, and format the data for subsequent
insertion into a database. The script is accessed by the seed.py
script.

Note: This script is not appropriate for use with the draft second version 
of the test directory due to the additional fields included in that file.

Functions:
    Get data as a dictionary of pandas dataframes
    Remove any completely blank rows
    Rename columns to be more programming-friendly
    Replace NaN values caused by merged cells in the original file
    Add additional requested fields
    Combine worksheets into a single dataframe
    Replace any newline characters with spaces
    Set default values for blank cells
    Convert all cells into strings and remove excess whitespace
    Convert cells in the 'targets' column into lists of targets

Inputs:
    filepath: path to .xlsx file containing NGTDC version 1 or 2 data

Returns:
    single_df [pandas dataframe]: cleaned data in dataframe format

"""


import pandas as pd


class Data:
    def __init__(self, filepath):
        self.filepath = filepath


    def get_xl_data(self, filepath):
        """
        Accesses an .xlsx file containing data for version 1 or 2 of the
        NGTDC, and converts each worksheet into a pandas dataframe.
        Creates a dictionary of these dataframes named df_dict.

        Args:
            filepath: path to .xlsx file containing NGTDC data

        Returns:
            df_dict [dict]: dictionary of pandas DataFrames
                keys: worksheet name e.g. 'Sarcomas'
                values: dataframe of columns A-H from relevant worksheet
        """

        # Specify which worksheets to access
        worksheets = [
            'Solid Tumours (Adult)',
            'Neurological tumours',
            'Sarcomas',
            'Haematological Tumours',
            'Paediatric',
        ]

        # Convert specified worksheets to dataframes and save in a dictionary
        df_dict = pd.read_excel(
            filepath,
            worksheets,
            usecols='A:H',
        )

        return df_dict


    def rename_columns(self, df_dict):
        """
        Renames dataframe columns to make them more programming-friendly
        (i.e. no spaces or parentheses).

        Args:
            df_dict [dict]: dictionary of pandas DFs containing NGTDC data

        Returns:
            df_dict [dict]: columns have been renamed across DFs
        """

        # Create a list of the new column names
        renamed_columns = [
            'ci_code',
            'ci_name',
            'test_code',
            'test_name',
            'targets_essential',
            'test_scope',
            'technology',
            'eligibility',
        ]

        # Iterate over each DF in the dict
        for df in df_dict:
            data = df_dict[df]

            # Rename the DF's columns
            data.columns = renamed_columns

        return df_dict


    def remove_blank_rows(self, df_dict):
        """
        Removes any rows in which all cells have NaN values.

        Args:
            df_dict [dict]: dictionary of pandas DFs containing NGTDC data

        Returns:
            df_dict [dict]: blank rows removed from each DF
        """

        for df in df_dict:
            data = df_dict[df]

            # Remove any row where all cells are blank
            data.dropna(
                axis=0,
                how='all',
                inplace=True,
            )

            # Reset the DF's row index to be a consistent series
            data.index = range(len(data))

        return df_dict


    def replace_merged_cells(self, df_dict):
        """
        Columns A and B (clinical indication code and name) contain
        merged cells in the .xlsx files, which translate to 'NaN' values
        in the DFs. This function replaces those NaN values with the
        appropriate value.

        Args:
            df_dict [dict]: dictionary of pandas DFs containing NGTDC data

        Returns:
            df_dict [dict]: previously merged empty cells now have values
        """

        for df in df_dict:
            data = df_dict[df]

            # Iterate over the rows of the current DF
            i = 0
            for index, row in data.iterrows():

                # iIf ci_code is blank in the current row,
                if pd.isna(row['ci_code']):

                    # update that cell to the value of the cell above it
                    data.loc[i, 'ci_code'] = data.loc[i-1, 'ci_code']

                    # similarly update the row's ci_name cell
                    data.loc[i, 'ci_name'] = data.loc[i-1, 'ci_name']

                i += 1

        return df_dict


    def add_new_fields(self, df_dict):
        """
        Creates 3 additional fields for each row in each DF:

        -cancer_type: the name of the parent worksheet e.g. 'Sarcomas'
        -in_house_test: currently 'Not specified' for all tests
        -currently_provided: currently 'Not specified' for all tests

        Args:
            df_dict [dict]: dictionary of pandas DFs containing NGTDC data

        Returns:
            df_dict [dict]: new fields have been added to each dataframe
        """

        # Use df_dict.keys to access the worksheet names
        for df in df_dict.keys():
            data = df_dict[df]

            # Define a default value for currently_provided and in_house_test
            default_value = 'Not specified'

            # Get the worksheet name for the current DF
            key = str(df).strip()

            # Set cancer type values to be consistent
            if 'neurological' in key.lower():
                cancer_type = 'Neurological Tumours'

            elif 'paediatric' in key.lower():
                cancer_type = 'Solid Tumours (Paediatric)'

            else:
                cancer_type = key

            # Create the fields and set their values for every cell in the DF
            data['cancer_type'] = cancer_type
            data['in_house_test'] = default_value
            data['currently_provided'] = default_value

        return df_dict


    def combine_dataframes(self, df_dict):
        """
        Combines all of the DFs in df_dict into a single dataframe.

        Args:
            df_dict [dict]: dictionary of pandas DFs containing NGTDC data

        Returns:
            single_df [pandas df]: a single DF, created by concatenating all
                the DFs in df_dict
        """

        # Combine all the DFs in df_dict into a single dataframe
        single_df = pd.concat(
            df_dict,
            ignore_index=True,
            keys=df_dict.keys(),
        )

        return single_df


    def default_blank_values(self, single_df):
        """
        Set the value of all empty cells to be 'Not specified'.

        Args:
            single_df [pandas df]: dataframe containing NGTDC data

        Returns:
            single_df [pandas df]: blank cells replaced with a default value
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
        Deals with cells in the targets column which have the value 'Not
        specified'; converts them to a single-element list.
        """

        # Define the new list value to be used
        new_value = ['Not specified', ]

        # Iterate over each row and look at the 'targets' field
        for index, row in single_df.iterrows():
            cell = row['targets_essential']

            # If a cell's value is 'Not specified', replace it
            if cell == 'Not specified':
                single_df.loc[index, 'targets_essential'] = new_value

        return single_df


    def target_lists_sublists(self, single_df):
        """
        Deals with cells in the targets column which have awkward commas;
        converts them to a single-element list.
        """

        # Iterate over each row and look at the 'targets' field
        for index, row in single_df.iterrows():

            # Ignore any rows which already have lists of targets
            if type(row['targets_essential']) == list:
                continue

            # Define cell to look at, convert to uppercase
            cell = row['targets_essential']
            uppercase = str(cell).upper()

            # If the cell is an awkward case,
            # (Note: must be 'types' not 'type' to exclude 'karyotype')
            if ('TRANSCRIPTS' in uppercase) or \
                ('TYPES' in uppercase) or \
                (uppercase == '1P, 3, 6, 8'):

                # Make the cell's value the sole element of a new list
                new_value = [uppercase, ]

                # Replace the original string value with this value
                single_df.loc[index, 'targets_essential'] = new_value

        return single_df


    def target_lists_other(self, single_df):
        """
        The main function for converting target cell strings to lists. There
        are still several awkward cases which need cleaning, like cells
        containing the PAR1 region, those with unnecessary text, or those
        with inappropriate brackets.

        There is a lot to do here, so this function is a bit of a monster.
        """

        # Iterate over each row
        for index, row in single_df.iterrows():
            
            # Ignore any rows which already have lists of targets
            if type(row['targets_essential']) == list:
                continue

            # Define cell to look at, convert to uppercase
            cell = row['targets_essential']
            uppercase = str(cell).upper()

            # Initialise a new empty list to be the output
            new_cell_list = []

            # If the cell contains the PAR1 region (awkward because it has
            # a sublist), extract this substring to be the first element of
            # the new list. Then deal with the cell remainder separately.

            par1_region = 'PAR1 REGION (CRLF2, CSF2RA, IL3RA)'

            if par1_region in uppercase:
                new_cell_list.append(par1_region)
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

            # Now go through and clean each element of this list 

            for element in old_cell_list:

                # Strip excess whitespace from each element
                stripped = element.strip()

                # Ignore any elements which are empty strings
                if stripped == '':
                    continue

                # Get rid of any unnecessary brackets in each element:
                # If the string is fully contained in brackets,

                elif ((stripped[0] == '(') and (stripped[-1] == ')')) or \
                        ((stripped[0] == '[') and (stripped[-1] == ']')):

                    target = stripped[1:-1]
                    new_cell_list.append(target)

                # If the string starts with an unpaired bracket,

                elif ((stripped[0] == '[') and (']' not in stripped)) or \
                        ((stripped[0] == '(') and (')' not in stripped)):

                    target = stripped[1:]
                    new_cell_list.append(target)

                # Or if the string ends with an unpaired bracket.

                elif ((stripped[-1] == ']') and ('[' not in stripped)) or \
                        ((stripped[-1] == ')') and ('(' not in stripped)):

                    target = stripped[:-1]
                    new_cell_list.append(target)

                else:
                    target = stripped
                    new_cell_list.append(target)

            # Finally, replace cell value with final list of cleaned elements

            single_df.loc[index, 'targets_essential'] = new_cell_list

        return single_df


    def UNUSED_scopes_to_lists(self, single_df):
        """Iterates over column 5 (test_scope) and changes each cell to a
        list, each element of which is a string representing a single scope
        of the test. If a cell is empty, it is changed to a single-element
        list. 

        Args:
            single_df [pandas df]: dataframe containing NGTDC data

        Returns:
            single_df [pandas df]: cells in column 5 are now lists
        """

        i = 0
        for row in single_df.iterrows():
            scope = row[1]['test_scope']
            new_cell = []

            if pd.isna(scope):
                new_cell.append('Not applicable')

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
            single_df [pandas df]: dataframe containing NGTDC data

        Returns:
            single_df [pandas df]: cells in column 6 are now lists
        """

        i = 0
        for row in single_df.iterrows():
            technology = row[1]['technology']
            new_cell = []

            if pd.isna(technology):
                new_cell.append('Not applicable')

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
