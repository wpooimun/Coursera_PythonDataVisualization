import week_2.project_isp_plot as target
from pprint import pprint
import unittest

gdpinfo = {
    "gdpfile": "../isp_gdp.csv",
    "separator": ",",
    "quote": '"',
    "min_year": 1960,
    "max_year": 2015,
    "country_name": "Country Name",
    "country_code": "Country Code"
}


class TestProjectIspPlot(unittest.TestCase):
    def test_read_csv_as_nested_dict(self):
        dct = target.read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])
        # pprint(dct)
        self.assertIsInstance(dct, dict)
        for row in dct.values():
            self.assertIsInstance(row, dict)

