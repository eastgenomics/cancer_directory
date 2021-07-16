#!usr/bin/env python

"""
Script function:
    1. Extract data from the National Genomic Test Directory for Cancer (NGTDC)
    2. Clean up data
        Remove any completely blank rows
        Replace NaN values caused by merged cells
        Rename columns to remove whitespace/parentheses
        Add a new 'cancer type' column based on worksheet name
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
        df_dict = pd.read_excel(filepath, sheets, usecols = 'A:H')

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

        return df_dict


    def replace_merged_cells(self, df_dict):
        """Columns A and B (clinical indication code and name) contain merged
        cells, which translate to 'NaN' values in df_dict. This function
        replaces the NaN values from merged cells with the appropriate value.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: empty cells caused by merging given relevant values
        """

        for df in df_dict:
            data = df_dict[df]
            ci_codes_column = data.iloc[:, 0]

            i = 0
            for cell in ci_codes_column:

                # if cell was merged in the xls worksheet,
                if pd.isna(cell):

                    # update cell value to that of the cell above it
                    data.iloc[i, 0] = data.iloc[i-1, 0]

                    # similarly update adjacent cell in column 1 (ci_name)
                    data.iloc[i, 1] = data.iloc[i-1, 1]

                i += 1

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
            'ci_code',
            'ci_name',
            'test_code',
            'test_name',
            'targets',
            'test_scope',
            'technology',
            'eligibility',
            ]

        for df in df_dict:
            data = df_dict[df]
            
            # Rename dataframe columns
            data.columns = renamed_columns

        return df_dict


    def sheetname_as_field(self, df_dict):
        """Creates a new field for generic cancer type in each df. Value is the
        name of the df.

        Args:
            df_dict [dict]: dictionary of pandas dfs containing NGTDC data

        Returns:
            df_dict [dict]: new cancer type field added to each dataframe
        """

        # Use df_dict.keys to access worksheet names
        for df in df_dict.keys():
            data = df_dict[df]

            cancer_type = str(df).strip()

            # Create new column 'cancer_type', set every cell to worksheet name
            data['cancer_type'] = cancer_type

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
        single_df.applymap(lambda x: str(x).strip())

        return single_df


    def targets_to_lists(self, single_df):
        """Each cell in column 4 ('targets') is currently a string, and needs
        to be converted into a list. Each element of the list should be a
        string representing a single target from that cell.

        e.g. 'NTRK1, NTRK2, NTRK3' becomes ['NTRK1', 'NTRK2', 'NTRK3']

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
            single_df [pandas df]: cells in column 4 are now lists
        """

        targets_column = single_df.iloc[:, 4]

        i = 0
        for cell in targets_column:
            uppercase = str(cell).upper()

            # If a cell is empty, give it a set value
            if pd.isna(cell):
                new_cell_contents = ['NOT APPLICABLE']


            # If splitting on ',' is a problem, take the whole cell
            # (Note: must be 'types' rather than 'type' to exclude 'karyotype')
            elif ('TRANSCRIPTS' in uppercase) or \
                ('TYPES' in uppercase) or \
                ('MLPA' in single_df.iloc[i, 6]):

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
            single_df.iloc[i, 4] = new_cell_contents
                
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

        scopes_column = single_df.iloc[:, 5]

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
            
            single_df.iloc[i, 5] = new_cell
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

        tech_column = single_df.iloc[:, 6]

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
            
            single_df.iloc[i, 6] = new_cell
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

            string_fields = ['cancer_type', 'ci_code', 'ci_name', 'test_code',
                    'test_name', 'eligibility']
            list_fields = ['targets', 'test_scope', 'technology']

            # print total, empty and unique cells
            for field in string_fields:
                column = data[field]
                elements = str(len(column))
                unique = str(len(column.unique()))
                empty = str(column.isnull().sum())

                print('{a} has length {b}, {c} are unique, {d} are empty'\
                    .format(a=field, b=elements, c=unique, d=empty))

            # or just print total and empty cells if field cells are lists
            for field in list_fields:
                column = data[field]
                elements = str(len(column))
                empty = str(column.isnull().sum())

                print('{a} has length {b}, {c} are empty'\
                    .format(a=field, b=elements, c=empty))

            # check that in each row, ci_code no. == test_code no.
            for i in range(len(data['test_code'])):
                ci_no_m = data.iloc[i, 0].replace('M', '')
                test_no_m = data.iloc[i, 2].replace('M', '')
                test_no_decimal = test_no_m.split('.')

                if ci_no_m != test_no_decimal[0]:
                    print('ci code/test code problem on line ' + str(i))


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
            cc_no_m = single_df.iloc[i, 0].replace('M', '')
            tc_no_m = single_df.iloc[i, 2].replace('M', '')
            tc_no_decimal = tc_no_m.split('.')

            if cc_no_m != tc_no_decimal[0]:
                print('ci code/test code problem on line ' + str(i))
        
        # get the numbers of distinct values in each field
        for column in single_df.columns:
            if column != 'targets':
                unique = single_df[column].unique()
                count = len(unique)
                print(
                    '\n{a} has {b} unique values'.format(a = column, b = count)
                    )
                print(unique[:20])
            
            else:
                unique = []
                for cell in single_df[column]:
                    for element in cell:
                        if element not in unique:
                            unique.append(element)
                count = len(unique)
                print(
                    '\n{a} has {b} unique values'.format(a = column, b = count)
                    )
                print(unique[:20])

        # # check list of individual targets
        # targets = []
        # for cell in single_df.iloc[:, 4]:
        #     for target in cell:
        #         if target not in targets:
        #             targets.append(target)
        
        # for target in targets:
        #     print(target)
