import week_4.project_isp_maps as target
from pprint import pprint
import unittest
import pygal


gdpinfo = {
    "gdpfile": "../isp_gdp.csv",
    "separator": ",",
    "quote": '"',
    "min_year": 1960,
    "max_year": 2015,
    "country_name": "Country Name",
    "country_code": "Country Code"
}

codeinfo = {
    "codefile": "../isp_country_codes.csv",  # Name of the country code CSV file
    "separator": ",",  # Separator character in CSV file
    "quote": '"',  # Quote character in CSV file
    "plot_codes": "ISO3166-1-Alpha-2",  # Plot code field name
    "data_codes": "ISO3166-1-Alpha-3"  # GDP data code field name
}


# Get pygal country code map
pygal_countries = pygal.maps.world.COUNTRIES


class TestProjectIspPlot(unittest.TestCase):
    def test_read_csv_as_nested_dict(self):
        dct = target.read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])
        # pprint(dct)
        self.assertIsInstance(dct, dict)
        for row in dct.values():
            self.assertIsInstance(row, dict)

    def test_build_country_code_converter(self):
        dct = target.build_country_code_converter(codeinfo)
        # pprint(dct)
        self.assertIsInstance(dct, dict)
        for key, val in dct.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(val, str)

    def test_reconcile_countries_by_code(self):
        # plot_countries = target.read_csv_as_nested_dict(codeinfo["codefile"], codeinfo['plot_codes'], codeinfo["separator"], codeinfo["quote"])
        # print(plot_countries)
        # print(pygal_countries)
        gdp_data = target.read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"], gdpinfo["separator"], gdpinfo["quote"])
        gdp_countries = dict((code, "") for code in gdp_data.keys())
        code_gdp_dict, missing_set = target.reconcile_countries_by_code(codeinfo, pygal_countries, gdp_countries)
        self.assertEqual(len(missing_set), 8)

    def test_build_map_dict_by_code(self):
        year = '1961'
        code_gdp_dict, missing_set, null_set = target.build_map_dict_by_code(gdpinfo, codeinfo, pygal_countries, year)
        # self.assertEqual(len(code_gdp_dict) + len(null_set), 154)
