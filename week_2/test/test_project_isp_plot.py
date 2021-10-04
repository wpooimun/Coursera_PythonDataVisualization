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

    def test_build_plot_values(self):
        dct = target.read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])
        for gdpdata in dct.values():
            lst = target.build_plot_values(gdpinfo, gdpdata)
            # print(lst)
            self.assertIsInstance(lst, list)
            for item in lst:
                self.assertIsInstance(item, tuple)
                self.assertIsInstance(item[0], int)
                self.assertIsInstance(item[1], float)

    def test_build_plot_dict(self):
        dct = target.read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])
        country_list = list(dct.keys())
        # print(country_list)
        dct = target.build_plot_dict(gdpinfo, country_list)
        # print(dct)
        self.assertIsInstance(dct, dict)
        for lst in dct.values():
            self.assertIsInstance(lst, list)
            for item in lst:
                self.assertIsInstance(item, tuple)
                # print(item)
                self.assertIsInstance(item[0], int)
                self.assertIsInstance(item[1], float)

    def test_render_xy_plot(self):
        dct = target.read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])
        country_list = list(dct.keys())
        # print(country_list)
        plot_file = "../plot.svg"
        target.render_xy_plot(gdpinfo, country_list, plot_file)
