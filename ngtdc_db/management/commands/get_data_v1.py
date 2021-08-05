#!usr/bin/env python

"""
National Genomic Test Directory for Cancer (NGTDC) *VERSION 1*

Script function:
    Extract data from the NGTDC
    Remove any completely blank rows
    Rename columns to remove whitespace/parentheses
    Replace NaN values caused by merged cells
    Set default values for blank cells
    Add new fields for in-house test and whether currently provided
    Combine worksheets into a single dataframe
    Convert all cells into strings and remove excess whitespace
    Convert cells in the 'targets' column into lists of targets

Inputs:
    An .xlsx file of the NGTDC

Returns:
    single_df: pandas dataframe with information on each test

"""

import pandas as pd


class Data:
    def __init__(self, filepath):
        self.filepath = filepath


    def get_xl_data(self, filepath):
        """Retrieves the 5 worksheets of test data from the NGTDC.

        Args:
            excel_file [xlsx file]: file containing the NGTDC

        Returns:
            df_dict [dict]: dictionary of pandas DataFrames
                keys: df name e.g. 'Sarcomas'
                values: dataframe of columns A-H from relevant worksheet
        """

        # Create list of df names
        sheets = [
            'Solid Tumours (Adult)',
            'Neurological tumours',
            'Sarcomas',
            'Haematological Tumours',
            'Paediatric',
            ]

        # Create pandas object with dfs as columns A-H of each worksheet
        df_dict = pd.read_excel(filepath, sheets, usecols='A:H')

        return df_dict


    def remove_blank_rows(self, df_dict):
        """Removes any rows where all cells have NaN values.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: blank rows removed from each df
        """

        for df in df_dict:
            data = df_dict[df]

            # Remove rows where all cells are blank
            data.dropna(axis=0, how='all', inplace=True)

            # Reset row index to be a consistent series
            data.index = range(len(data))

        return df_dict


    def rename_columns(self, df_dict):
        """Renames the columns to make them easier to work with (some
        original column names contain spaces and parentheses).

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: columns renamed in each df
        """

        # Create list of new column names
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

        for df in df_dict:
            data = df_dict[df]
            
            # Rename dataframe columns
            data.columns = renamed_columns

        return df_dict


    def replace_merged_cells(self, df_dict):
        """Columns A and B (clinical indication code and name) contain
        merged cells, which translate to 'NaN' values in df_dict. This
        function replaces the NaN values from merged cells with the
        appropriate value.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: values assigned to empty cells caused by merging
        """

        for df in df_dict:
            data = df_dict[df]
            ci_codes_column = data.loc[:, 'ci_code']

            i = 0
            for cell in ci_codes_column:

                # if cell was merged in the xls worksheet,
                if pd.isna(cell):

                    # update cell value to that of the cell above it
                    data.loc[i, 'ci_code'] = data.loc[i-1, 'ci_code']

                    # similarly update adjacent cell in column 1 (ci_name)
                    data.loc[i, 'ci_name'] = data.loc[i-1, 'ci_name']

                i += 1

        return df_dict


    def default_blank_values(self, df_dict):
        """Set the value of all empty cells to be 'Not specified'.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: blank cells replaced with default value
        """

        for df in df_dict:

            # Define the default value for blank cells
            blank_value = 'Not specified'

            # Set all empty cells to the default value
            df_dict[df].fillna(blank_value, inplace=True)

            # Set cells which strip to a blank string to the default value
            df_dict[df] = df_dict[df].applymap(
                lambda x: 'Not specified' if str(x).strip() == '' else x
                )

        return df_dict


    def add_new_fields(self, df_dict):
        """Creates 3 additional fields for each test in each df:

        -cancer_type: the name of the parent dataframe e.g. 'Sarcomas'
        -in_house_test: currently 'Not specified' for all tests
        -currently_provided: currently 'Not specified' for all tests

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: new fields added to each dataframe
        """

        # Use df_dict.keys to access worksheet names
        for df in df_dict.keys():
            data = df_dict[df]

            # Get field value for current df
            key = str(df).strip()

            if 'neurological' in key.lower():
                cancer_type = 'Neurological Tumours'

            elif 'paediatric' in key.lower():
                cancer_type = 'Solid Tumours (Paediatric)'
            
            else:
                cancer_type = key
            
            default_value = 'Not specified'

            # Create new fields and set values for every cell
            data['cancer_type'] = cancer_type
            data['in_house_test'] = default_value
            data['currently_provided'] = default_value

        return df_dict


    def combine_dataframes(self, df_dict):
        """Combines the multiple dataframes in df_dict into one.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            single_df [pandas df]: created by concatenating dfs in df_dict
        """

        # Combine all dataframes from df_dict into one
        single_df = pd.concat(
            df_dict,
            ignore_index = True,
            keys = df_dict.keys(),
            )

        return single_df


    def all_cells_to_strings(self, single_df):
        """Converts all cells in single_df into strings, strips excess
        whitespace.

        Args:
            single_df [pandas df]: contains NGTDC data

        Returns:
            single_df [pandas df]: all cells changed to stripped strings
        """

        # convert every cell value to a string, and strip whitespace
        single_df = single_df.applymap(str)
        single_df = single_df.applymap(lambda x: x.strip())

        return single_df


    def targets_to_lists(self, single_df):
        """Each cell in column 4 ('targets') is currently a string, and
        needs to be converted into a list. Each element of the list should
        be a string representing a single target from that cell.

        e.g. 'NTRK1, NTRK2, NTRK3' becomes ['NTRK1', 'NTRK2', 'NTRK3']

        Text is converted to uppercase to avoid duplication issues 
        (e.g. '1q2' vs. '1Q2').

        Some cells are awkward and need to be managed separately:
        -Empty cells become ['NOT APPLICABLE']
        -Targets which contain sub-lists have to be kept as a whole string
        -Paired brackets around a target, or unpaired brackets at a target
        end, are removed

        Args:
            single_df [pandas df]: contains NGTDC data

        Returns:
            single_df [pandas df]: cells in column 4 are now lists
        """

        targets_column = single_df['targets_essential']

        i = 0
        for cell in targets_column:
            uppercase = str(cell).upper()

            # If cell value isn't specified, make it a single-element list
            if cell == 'Not specified':
                new_cell_contents = ['Not specified',]

            # If splitting on ',' is a problem, take the whole cell
            # (Note: must be 'types' rather than 'type' to exclude 'karyotype')
            elif ('TRANSCRIPTS' in uppercase) or \
                ('TYPES' in uppercase) or \
                ('MLPA' in single_df.iloc[i].loc['technology']):

                new_cell_contents = [uppercase]

            # For cells which are a 'standard' list of targets:
            else:
                new_cell_contents = []

                # If a cell contains the PAR1 region (awkward due to commas),
                par1_region = 'PAR1 REGION (CRLF2, CSF2RA, IL3RA)'

                if par1_region in uppercase:                

                    # Add this region to the cell's new list separately
                    new_cell_contents.append(par1_region)

                    # Remove it from the old cell value
                    cell_contents = uppercase.replace(par1_region, '')

                else:
                    cell_contents = uppercase

                # If the cell contains unnecessary preamble, remove it
                if 'TO INCLUDE DETECTION OF' in cell_contents:
                    to_split = cell_contents.replace(
                        'TO INCLUDE DETECTION OF', '')

                elif 'TO INCLUDE:' in cell_contents:
                    to_split = cell_contents.replace('TO INCLUDE:', '')

                elif 'TO INCLUDE' in cell_contents:
                    to_split = cell_contents.replace('TO INCLUDE', '')

                elif 'E.G.' in cell_contents:
                    to_split = cell_contents.replace('E.G.', '')

                else:
                    to_split = cell_contents

                # Split cell contents into a list on a comma delimiter
                old_cell_target_list = to_split.split(',')

                for element in old_cell_target_list:
                    # Strip whitespace, then skip any blank elements
                    stripped = element.strip()
                    if stripped == '':
                        continue

                    # If an element is contained in  brackets, remove them
                    elif ((stripped[0] == '(') and (stripped[-1] == ')')) or \
                        ((stripped[0] == '[') and (stripped[-1] == ']')):

                        target = stripped[1:-1]
                        new_cell_contents.append(target)

                    # If an element starts with an unpaired bracket, remove it
                    elif ((stripped[0] == '[') and (']' not in stripped)) or \
                        ((stripped[0] == '(') and (')' not in stripped)):

                        target = stripped[1:]
                        new_cell_contents.append(target)

                    # If an element ends with an unpaired bracket, remove it
                    elif ((stripped[-1] == ']') and ('[' not in stripped)) or \
                        ((stripped[-1] == ')') and ('(' not in stripped)):

                        target = stripped[:-1]
                        new_cell_contents.append(target)

                    # Otherwise just append to cell's new list
                    else:
                        target = stripped
                        new_cell_contents.append(target)

            # Replace cell's old string value with new_cell_contents list
            single_df.iloc[i].loc['targets_essential'] = new_cell_contents
                
            i += 1

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
            single_df [pandas df]: contains NGTDC data

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
