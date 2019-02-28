from unittest import TestCase
from mpr.data.api.purchase import parse_attributes


class TestPurchase(TestCase):
    def test_objects_are_the_same(self):
        first = parse_attributes({
            'reported_for_date': '01/02/2018',
            'report_date': '01/03/2018',
            'purchase_type': 'Negotiated (carcass basis)',
            'head_count': '14,141',
            'price_low': '48.00',
            'price_high': '52.00',
            'wtd_avg': '50.00'
        })

        second = parse_attributes({
            'reported_for_date': '01/02/2018',
            'report_date': '01/03/2018',
            'purchase_type': 'Negotiated (carcass basis)',
            'head_count': '0'
        })

        self.assertEqual(hash(first), hash(second))

    def test_objects_are_not_the_same(self):
        first = parse_attributes({
            'reported_for_date': '01/02/2018',
            'report_date': '01/03/2018',
            'purchase_type': 'Negotiated Formula (carcass basis)',
            'head_count': '0'
        })

        second = parse_attributes({
            'reported_for_date': '01/02/2018',
            'report_date': '01/03/2018',
            'purchase_type': 'Negotiated Formula (live basis)',
            'head_count': '0'
        })

        self.assertNotEqual(hash(first), hash(second))

    def test_contents_are_the_same(self):
        first = parse_attributes({
            'reported_for_date': '01/02/2018',
            'report_date': '01/03/2018',
            'purchase_type': 'Negotiated (carcass basis)',
            'head_count': '14,141',
            'price_low': '48.00',
            'price_high': '52.00',
            'wtd_avg': '50.00'
        })

        second = parse_attributes({
            'reported_for_date': '01/02/2018',
            'report_date': '01/03/2018',
            'purchase_type': 'Negotiated (carcass basis)',
            'head_count': '14,141',
            'price_low': '48.00',
            'price_high': '52.00',
            'wtd_avg': '50.00'
        })

        self.assertEqual(first, second)

    def test_contents_are_not_the_same(self):
        first = parse_attributes({
            'reported_for_date': '01/02/2018',
            'report_date': '01/03/2018',
            'purchase_type': 'Negotiated (carcass basis)',
            'head_count': '14,141',
            'price_low': '48.00',
            'price_high': '52.00',
            'wtd_avg': '50.00'
        })

        second = parse_attributes({
            'reported_for_date': '01/02/2018',
            'report_date': '01/03/2018',
            'purchase_type': 'Negotiated (carcass basis)',
            'head_count': '14,141'
        })

        self.assertNotEqual(first, second)
