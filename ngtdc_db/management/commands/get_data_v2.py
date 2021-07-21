#!usr/bin/env python

"""
National Genomic Test Directory for Cancer (NGTDC) *VERSION 2*

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
            filepath: path to xlsx file containing the NGTDC

        Returns:
            df_dict [dict]: dictionary of pandas DataFrames
                key: df name e.g. 'Sarcomas'
                value: dataframe of columns B-P from relevant worksheet
        """

        # Create list of worksheet names
        sheets = [
            'Solid Tumours (2)',
            'Neurological tumours (2)',
            'Sarcoma (2)',
            'Haematological (2)',
            'Paediatric (2)',
            ]

        # Create pandas object with dfs as columns A-P of each worksheet
        df_dict = pd.read_excel(filepath, sheets, usecols = 'B:P')

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
            data.dropna(axis = 0, how = 'all', inplace = True)

            # Reset row index to be a consistent series
            data.index = range(len(data))

        return df_dict


    def rename_columns(self, df_dict):
        """Renames the columns to make them easier to work with (some original
        column names contain spaces and parentheses)

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: columns renamed in each df
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


    def replace_merged_cells(self, df_dict):
        """Columns B-E (tumour group, specialist test group, CI code and name)
        contain merged cells, which translate to 'NaN' values in df_dict. This
        function replaces the NaN values from merged cells with the appropriate
        value.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: empty cells caused by merging given relevant values
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

                    # similarly update adjacent cells in cols B, C, E
                    data.loc[i, 'cancer_type'] = data.loc[i-1, 'cancer_type']

                    data.loc[i, 'specialist_group'] = data.loc[i-1,
                        'specialist_group']

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

            # Set all empty cells (or just whitespace) to default
            df_dict[df].fillna(blank_value, inplace=True)
            df_dict[df] = df_dict[df].applymap(
                lambda x: 'Not specified' if str(x).strip() == '' else x
                )

        return df_dict


    def TEMPORARY_FIX_BLANK_TCS(self, df_dict):
        """Because test_code is the primary key for the GenomicTest model, all
        records must have a unique value for this field. Version 2 of the test
        directory is problematic because many records have a blank test code
        value, meaning they all get assigned a non-unique value of 'Not
        specified' (thanks version 2). There is also an issue where two
        different tests have been assigned the test code 'M150.6'. This
        function removes any records where the test code is blank, and the two
        tests with the same test code.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: rows with test code = 'Not specified' removed
        """

        for df in df_dict:
            data = df_dict[df]

            # If a row has a test code value of 'Not specified', drop the row
            data.drop(data.loc[data['test_code']=='Not specified'].index,
                inplace=True)

            # If a row has a test code value of 'M150.6', drop the row
            data.drop(data.loc[data['test_code']=='M150.6'].index,
                inplace=True)

            # Reset row index to be a consistent series
            data = data.reset_index

        return df_dict


    def add_new_fields(self, df_dict):
        """Creates 2 additional fields for each test in each df:

        -in_house_test: currently 'Not specified' for all tests
        -currently_provided: currently 'Not specified' for all tests

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: new fields added to each dataframe
        """

        for df in df_dict:
            data = df_dict[df]

            default_value = 'Not specified'

            # Create new fields and set default values for every cell
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
            single_df [pandas df]: updated with all cells as stripped strings
        """

        # convert every cell value to a string, and strip whitespace
        single_df = single_df.applymap(lambda x: str(x).strip())

        return single_df


    def targets_to_lists(self, single_df):
        """Each cell in 'targets_essential' and 'targets_desirable' is
        currently a string, and needs to be converted into a list. Each element
        of the list should be a string representing a single target from that
        cell, e.g.
        
        'NTRK1, NTRK2, NTRK3' becomes ['NTRK1', 'NTRK2', 'NTRK3']

        Text is converted to uppercase to avoid duplication issues (e.g. '1q2'
        vs. '1Q2').

        Some cells are awkward and need to be managed separately:
        -Empty cells become ['NOT APPLICABLE']
        -Targets which contain sub-lists have to be kept as a whole string
        -Paired brackets around a target, or unpaired brackets at a target end,
        are removed

        Args:
            single_df [pandas df]: contains NGTDC data

        Returns:
            single_df [pandas df]: cells in targets columns are now lists
        """

        fields = ['targets_essential', 'targets_desirable']

        for field in fields:
            column = single_df[field]
            i = 0

            for cell in column:
                uppercase = str(cell).upper()

                # If a cell is empty, make it a single-element list
                if cell == 'Not specified':
                    new_cell_contents = ['Not specified',]


                # If splitting on ',' is a problem, take the whole cell
                # (Note: must be 'types' not 'type', to exclude 'karyotype')
                elif ('TRANSCRIPTS' in uppercase) or \
                    ('TYPES' in uppercase) or \
                    ('MLPA' in str(single_df.loc[i, 'technology'])):

                    new_cell_contents = [uppercase,]


                # For cells which are a 'standard' list of targets:
                else:
                    new_cell_contents = []


                    # If a cell contains PAR1 region (awkward due to commas),
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


                        # If element is contained in brackets, remove them
                        elif ((stripped[0] == '(') and (stripped[-1] == ')'))\
                                or \
                            ((stripped[0] == '[') and (stripped[-1] == ']')):

                            target = stripped[1:-1]
                            new_cell_contents.append(target)

                        # If element starts with an unpaired bracket, remove it
                        elif ((stripped[0] == '[') and (']' not in stripped))\
                                or \
                            ((stripped[0] == '(') and (')' not in stripped)):

                            target = stripped[1:]
                            new_cell_contents.append(target)

                        # If element ends with an unpaired bracket, remove it
                        elif ((stripped[-1] == ']') and ('[' not in stripped))\
                                or \
                            ((stripped[-1] == ')') and ('(' not in stripped)):

                            target = stripped[:-1]
                            new_cell_contents.append(target)


                        # Otherwise just append to cell's new list
                        else:
                            target = stripped
                            new_cell_contents.append(target)

                # Replace cell's old string value with new_cell_contents list
                single_df.iloc[i].loc[field] = new_cell_contents
                    
                i += 1

        return single_df


    def scopes_to_lists(self, single_df):
        """NOT CURRENTLY IN USE
        
        Iterates over column 5 (test_scope) and changes each cell to a list,
        each element of which is a string representing a single scope of the
        test. If a cell is empty, it is changed to a single-element list. 

        Args:
            single_df [pandas df]: contains NGTDC data

        Returns:
            single_df [pandas df]: cells in column 5 are now lists
        """

        scopes_column = single_df.loc[:, 'test_scope']

        i = 0
        for cell in scopes_column:
            new_cell = []
            if pd.isna(cell):
                new_cell.append('Not applicable')
            
            elif '/' in cell:
                scope_list = cell.split('/')
                stripped = [element.strip() for element in scope_list]
                for scope in stripped:
                    new_cell.append(scope)
            
            elif ';' in cell:
                scope_list = cell.split(';')
                stripped = [element.strip() for element in scope_list]
                for scope in stripped:
                    new_cell.append(scope)
            
            else:
                stripped = cell.strip()
                new_cell.append(stripped)
            
            single_df.loc[i, 'test_scope'] = new_cell
            i += 1

        return single_df


    def tech_to_lists(self, single_df):
        """NOT CURRENTLY IN USE
        
        Iterates over column 6 (technology) and changes each cell to a list,
        each element of which is a string representing a single technology. If
        a cell is empty, it is changed to a single-element list. 

        Args:
            single_df [pandas df]: contains NGTDC data

        Returns:
            single_df [pandas df]: cells in column 6 are now lists
        """

        tech_column = single_df.loc[:, 'technology']

        i = 0
        for cell in tech_column:
            new_cell = []
            if pd.isna(cell):
                new_cell.append('Not applicable')
            
            elif '/' in cell:
                tech_list = cell.split('/')
                stripped = [element.strip() for element in tech_list]
                for tech in stripped:
                    new_cell.append(tech)
            
            elif ';' in cell:
                tech_list = cell.split(';')
                stripped = [element.strip() for element in tech_list]
                for tech in stripped:
                    new_cell.append(tech)
            
            else:
                stripped = cell.strip()
                new_cell.append(stripped)
            
            single_df.loc[i, 'technology'] = new_cell
            i += 1

        return single_df


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


    def check_single_df(self, single_df):
        """Optional check on final dataframe contents

        Args:
            single_df [pandas df]: contains NGTDC data
        """

        print('\n')
        print(single_df.head(n=5))
        print('\n')
        print(single_df.tail(n=5))

        # check that in each row, ci_code and test_code have the same number
        for i in range(len(single_df['test_code'])):
            cc_no_m = str(single_df.iloc[i].loc['ci_code']).replace('M', '')
            tc_no_m = str(single_df.iloc[i].loc['test_code']).replace('M', '')
            tc_no_decimal = tc_no_m.split('.')

            if cc_no_m != tc_no_decimal[0]:
                print(
                    'ci code/test code problem on line', str(i), ':',
                    single_df.iloc[i].loc['ci_code'],
                    single_df.iloc[i].loc['test_code']
                    )

        # get the numbers of distinct values in each field
        exclude_fields = ['targets_essential', 'targets_desirable']

        for field in single_df.columns:
            if field not in exclude_fields:
                unique = single_df[field].unique()
                count = len(unique)

                print(
                    '\n{a} has {b} unique values'.format(a = field, b = count)
                    )
                print(unique[:20])
            
            else:
                unique = []
                for cell in single_df[field]:
                    for element in cell:
                        if (element != '') and (element not in unique):
                            unique.append(element)
                
                count = len(unique)
                print(
                    '\n{a} has {b} unique values'.format(a = field, b = count)
                    )
                
                # for element in unique:
                #     print(element)
