"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
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


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    code_converter_dict = dict()
    filename = codeinfo["codefile"]
    keyfield = codeinfo['plot_codes']
    separator = codeinfo["separator"]
    quote = codeinfo["quote"]
    dct_of_dct = read_csv_as_nested_dict(filename, keyfield, separator, quote)
    for dct in dct_of_dct.values():
        plot_code = dct[codeinfo['plot_codes']]
        data_code = dct[codeinfo['data_codes']]
        code_converter_dict[plot_code] = data_code
    return code_converter_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    codes = build_country_code_converter(codeinfo)
    plot_gdp_code_dict = dict()
    missing_set = set()
    # maps codes to lower case
    lc_plot_countries = dict((code.lower(), code) for code in plot_countries.keys())
    lc_gdp_countries = dict((code.lower(), code) for code in gdp_countries.keys())
    lc_code_converter_dict = dict((key.lower(), val.lower()) for key, val in codes.items())
    # compare and categorise the countries codes
    for lc_code, ori_code in lc_plot_countries.items():
        # print(lc_code, lc_code not in lc_gdp_countries.keys())
        if lc_code_converter_dict.get(lc_code) not in lc_gdp_countries.keys():
            missing_set.add(ori_code)
            # print(f"WARNING! Country name {country_name} not in GDP countries!")
        else:
            plot_gdp_code_dict[ori_code] = lc_gdp_countries[lc_code_converter_dict[lc_code]]
    print(f"Total of {len(missing_set)} Countries missing.")
    print(f"Total of {len(plot_gdp_code_dict)} Countries joined.")
    return plot_gdp_code_dict, missing_set


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    # prepare data
    filename = gdpinfo["gdpfile"]
    keyfield = gdpinfo['country_code']
    separator = gdpinfo["separator"]
    quote = gdpinfo["quote"]
    gdp_countries = read_csv_as_nested_dict(filename, keyfield, separator, quote)
    plot_gdp_code_dict, missing_set = reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)
    # build map dict
    code_gdp_dict = dict()
    null_set = set()
    for plot_code, gdp_code in plot_gdp_code_dict.items():
        country_data = gdp_countries[gdp_code]
        gdp = country_data[year]
        if gdp == "":
            null_set.add(plot_code)
        else:
            code_gdp_dict[plot_code] = math.log10(float(gdp))
    return code_gdp_dict, missing_set, null_set


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    code_gdp_dict, missing_set, null_set = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
    chart = pygal.maps.world.World()
    chart.title = f"GDP (log scale) in year {year}"
    # Filter countries according to gdp range
    max_min_trillion_dict = {
        "< 0.21": (0, 0.21),
        "0.21 - 0.75": (0.21, 0.75),
        "0.75 - 1.89":  (0.75, 1.89),
        "1.89 - 3.81": (1.89, 3.81),
        "> 3.81": (3.81, 10)
    }
    for label, minmaxrange in max_min_trillion_dict.items():
        temp_list = [
            country
            for country, gdp in code_gdp_dict.items()
            if minmaxrange[0] * 1e12 <= gdp < minmaxrange[1] * 1e12
        ]
        chart.add(label, temp_list)
    chart.add("Missing country from World Bank Data", missing_set)
    chart.add("Empty GDP from World Bank Data", null_set)
    chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
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

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()

