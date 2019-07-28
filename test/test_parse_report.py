from unittest import TestCase
from numpy import isnan
from numpy import isclose

from mpr.api import filter_sections
from mpr.api import opt_int
from mpr.api import opt_float
from mpr.reports import CutoutSection

from test import load_resource

elements = load_resource('api/cutout.xml')
records = filter_sections(elements, CutoutSection.CUTOUT, CutoutSection.VOLUME)
cutout, volume = next(records)


class ParseReportTest(TestCase):
    def test_parse_int(self):
        attr = {'volume': '1,234'}
        self.assertEqual(opt_int(attr, 'volume'), 1234)

    def test_parse_float(self):
        attr = {'weight': '1,234.56'}
        self.assertTrue(isclose(opt_float(attr, 'weight'), 1234.56))

    def test_opt_int(self):
        self.assertEqual(opt_int({}, 'volume'), 0)
        self.assertEqual(opt_int({'volume': 'null'}, 'volume'), 0)

    def test_opt_float(self):
        self.assertTrue(isnan(opt_float({}, 'volume')))
        self.assertTrue(isnan(opt_float({'weight': 'null'}, 'volume')))

    def test_volume_slug(self):
        self.assertEqual(volume['slug'], 'LM_PK603')

    def test_volume_date(self):
        self.assertEqual(volume['report_date'], '08/20/2018')

    def test_volume_label(self):
        self.assertEqual(volume['label'], 'Current Volume')

    def test_primal_loads(self):
        self.assertEqual(volume['temp_cuts_total_load'], '334.74')

    def test_trimming_loads(self):
        self.assertEqual(volume['temp_process_total_load'], '39.61')

    def test_cutout_slug(self):
        self.assertEqual(volume['slug'], 'LM_PK603')

    def test_cutout_date(self):
        self.assertEqual(cutout['report_date'], '08/20/2018')

    def test_cutout_label(self):
        self.assertEqual(cutout['label'], 'Cutout and Primal Values')

    def test_carcass_value(self):
        self.assertEqual(cutout['pork_carcass'], '67.18')

    def test_loin_value(self):
        self.assertEqual(cutout['pork_loin'], '75.51')

    def test_butt_value(self):
        self.assertEqual(cutout['pork_butt'], '89.55')

    def test_picnic_value(self):
        self.assertEqual(cutout['pork_picnic'], '41.82')

    def test_rib_value(self):
        self.assertEqual(cutout['pork_rib'], '113.95')

    def test_ham_value(self):
        self.assertEqual(cutout['pork_ham'], '57.52')

    def test_belly_value(self):
        self.assertEqual(cutout['pork_belly'], '77.77')