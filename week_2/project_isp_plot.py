"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    dct_of_dct = dict()
    # Perform action when file is opened
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            key = row[keyfield]
            dct_of_dct[key] = row
    return dct_of_dct


def build_plot_values(gdpinfo1, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    lst_of_tup = list()
    for key, val in gdpdata.items():
        # Error will appear if k cannot be converted to int or v cannot be converted to float
        try:
            key = int(key)
            if gdpinfo1["min_year"] <= key <= gdpinfo1["max_year"]:
                if val != "":
                    tup = (key, float(val))
                    lst_of_tup.append(tup)
        except ValueError:
            continue
    return lst_of_tup


def build_plot_dict(gdpinfo1, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    dct_of_tup = dict()
    csv_dct = read_csv_as_nested_dict(gdpinfo1["gdpfile"], gdpinfo1["country_name"], gdpinfo1["separator"],
                                         gdpinfo1["quote"])
    for country in country_list:
        # Check if country is in the dictionary before action
        gdpdata = csv_dct.get(country, None)
        if gdpdata is not None:
            plot_values = build_plot_values(gdpinfo1, gdpdata)
            plot_values.sort(key=lambda x: x[0])
            dct_of_tup[country] = plot_values
        else:
            dct_of_tup[country] = list()
    return dct_of_tup


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    plot_data = build_plot_dict(gdpinfo, country_list)
    chart = pygal.XY()
    chart.title = "GDP data"
    # Add plot of country iteratively
    for country in country_list:
        print(plot_data[country])
        chart.add(country, plot_data[country])
    chart.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

# test_render_xy_plot()