import week_3.project_isp_unify as target
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

# Get pygal country code map
pygal_countries = pygal.maps.world.COUNTRIES


class TestProjectIspPlot(unittest.TestCase):
    def test_read_csv_as_nested_dict(self):
        dct = target.read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])
        # pprint(dct)
        self.assertIsInstance(dct, dict)
        for row in dct.values():
            self.assertIsInstance(row, dict)

    def test_reconcile_countries_by_name(self):
        dct = target.read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])
        code_gdp_dict, missing_set = target.reconcile_countries_by_name(pygal_countries, dct)
        self.assertEqual(len(missing_set), 30)

    def test_build_map_dict_by_name(self):
        year = 1961
        code_gdp_dict, missing_set, null_set = target.build_map_dict_by_name(gdpinfo, pygal_countries, year)
        self.assertEqual(len(code_gdp_dict) + len(null_set), 154)
