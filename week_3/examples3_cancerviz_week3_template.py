"""
Week 3 practice project template for Python Data Visualization
Read two CSV files and join the resulting tables based on shared FIPS codes
Analyze both data sources for anamolous FIPS codes
"""

import csv


#########################################################
# Provided code for week 3

def print_table(table):
    """
    Echo a nested list to the console
    """
    for row in table:
        print(row)


def read_csv_file(file_name):
    """
    Given a CSV file, read the data into a nested list
    Input: String corresponding to comma-separated  CSV file
    Output: Nested list consisting of the fields in the CSV file
    """

    with open(file_name, newline='') as csv_file:  # don't need to explicitly close the file now
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_table.append(row)
    return csv_table


def write_csv_file(csv_table, file_name):
    """
    Input: Nested list csv_table and a string file_name
    Action: Write fields in csv_table into a comma-separated CSV file with the name file_name
    """

    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in csv_table:
            csv_writer.writerow(row)


# Part 1 - function that creates a dictionary from a table

def make_dict(table, key_col):
    """
    Given a 2D table (list of lists) and a column index key_col,
    return a dictionary whose keys are entries of specified column
    and whose values are lists consisting of the remaining row entries
    """
    dct = dict()
    for row_list in table:
        dct[row_list[key_col]] = [i for idx, i in enumerate(row_list) if idx != key_col]
    return dct


def test_make_dict():
    """
    Some tests for make_dict()
    """
    table1 = [[1, 2], [3, 4], [5, 6]]
    print(make_dict(table1, 0))
    print(make_dict(table1, 1))
    table2 = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
    print(make_dict(table2, 1))
    print(make_dict(table2, 2))


# test_make_dict()


# Part 2 - script for merging the CSV files

CANCER_RISK_FIPS_COL = 2
CENTER_FIPS_COL = 0


def merge_csv_files(cancer_csv_file, center_csv_file, joined_csv_file):
    """
    Read two specified CSV files as tables
    Join the these tables by shared FIPS codes
    Write the resulting joined table as the specified file
    Analyze for problematic FIPS codes
    """

    # Read in both CSV files
    cancer_csv_table = read_csv_file(cancer_csv_file)
    center_csv_table = read_csv_file(center_csv_file)

    # Compute joined table, print warning about cancer-risk FIPS codes that are not in USA map
    cancer_list_dict = make_dict(cancer_csv_table, 2)
    center_list_dict = make_dict(center_csv_table, 0)
    joined_table = list()
    missing_fips_list = list()
    for cancer_fips, lst in cancer_list_dict.items():
        if cancer_fips not in center_list_dict.keys():
            missing_fips_list.append(cancer_fips)
            print(f"WARNING! Cancer-risk FIPS code {cancer_fips} not in USA map!")
        else:
            joined_list = lst[:2] + [cancer_fips] + lst[2:] + center_list_dict[cancer_fips]
            joined_table.append(joined_list)
    print(f"Total of {len(joined_table)} Cancer-risk data joined.")

    # Write joined table
    write_csv_file(joined_table, "merged_csv.csv")

    # Print warning about FIPS codes in USA map that are missing from cancer risk data
    print(f"Total of {len(missing_fips_list)} Cancer-risk FIPS code not in USA map:")
    print(missing_fips_list)
    pass


merge_csv_files("cancer_risk_trimmed_solution.csv", "USA_Counties_with_FIPS_and_centers.csv", "cancer_risk_joined.csv")

## Part 3 - Explanation for anomalous FIPS codes

## https://www1.udel.edu/johnmack/frec682/fips_codes.html
##
## Output anamolies for cancer risk data
## Puerto Rico, Virgin Island, Statewide, Nationwide - FIPS codes are all not present on USA map
## One specific county (Clifton Forge, VA - 51560) is also not present in USA map.
## According URL above, Clifton Forge was merged with another VA county prior to 2001
##
## Output anamolies for USA map
## State_Line, separator - FIPS codes are all not present in cancer-risk data
## One specific county (Broomfield County - 08014) is also not present in cancer-risk data
## Accoring to URL above, Broomfield County was created in 2001
##
## Implies cancer risk FIPS codes were defined prior to 2001, the USA map FIPS codes were defined after 2001