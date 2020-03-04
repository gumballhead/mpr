from datetime import date
from numpy import isnan
from numpy import isclose

from mpr.purchase.api import parse_attributes
from mpr.purchase.model import to_array
from mpr.purchase_type import Seller, Arrangement, Basis

from test import load_resource

barrows_gilts = list(load_resource('api/purchase.xml'))
assert len(barrows_gilts) == 7

negotiated = parse_attributes(barrows_gilts[0])
negotiated_formula = parse_attributes(barrows_gilts[1])
market_formula = parse_attributes(barrows_gilts[3])
negotiated_live = parse_attributes(barrows_gilts[4])
negotiated_formula_live = parse_attributes(barrows_gilts[5])


def test_negotiated_purchase():
    assert negotiated.date == date(2019, 1, 31)
    assert negotiated.report_date == date(2019, 2, 1)
    assert negotiated.seller == Seller.ALL
    assert negotiated.arrangement == Arrangement.NEGOTIATED
    assert negotiated.basis == Basis.CARCASS
    assert negotiated.head_count == 11_325
    assert isclose(negotiated.avg_price, 50.70)
    assert isclose(negotiated.low_price, 48.00)
    assert isclose(negotiated.high_price, 51.75)


def test_negotiated_formula():
    assert negotiated_formula.date == date(2019, 1, 31)
    assert negotiated_formula.report_date == date(2019, 2, 1)
    assert negotiated_formula.seller == Seller.ALL
    assert negotiated_formula.arrangement == Arrangement.NEGOTIATED_FORMULA
    assert negotiated_formula.basis == Basis.CARCASS
    assert negotiated_formula.head_count == 165
    assert isnan(negotiated_formula.avg_price)
    assert isnan(negotiated_formula.low_price)
    assert isnan(negotiated_formula.high_price)


def test_market_formula():
    assert market_formula.date == date(2019, 1, 31)
    assert market_formula.report_date == date(2019, 2, 1)
    assert market_formula.seller == Seller.ALL
    assert market_formula.arrangement == Arrangement.MARKET_FORMULA
    assert market_formula.basis == Basis.CARCASS
    assert market_formula.head_count == 139_569
    assert isclose(market_formula.avg_price, 55.40)
    assert isclose(market_formula.low_price, 48.88)
    assert isclose(market_formula.high_price, 63.83)


def test_negotiated_live():
    assert negotiated_live.date == date(2019, 1, 31)
    assert negotiated_live.report_date == date(2019, 2, 1)
    assert negotiated_live.seller == Seller.ALL
    assert negotiated_live.arrangement == Arrangement.NEGOTIATED
    assert negotiated_live.basis == Basis.LIVE
    assert negotiated_live.head_count == 703
    assert isclose(negotiated_live.avg_price, 39.92)
    assert isclose(negotiated_live.low_price, 34.00)
    assert isclose(negotiated_live.high_price, 41.75)


def test_negotiated_formula_live():
    assert negotiated_formula_live.date == date(2019, 1, 31)
    assert negotiated_formula_live.report_date == date(2019, 2, 1)
    assert negotiated_formula_live.seller == Seller.ALL
    assert negotiated_formula_live.arrangement == Arrangement.NEGOTIATED_FORMULA
    assert negotiated_formula_live.basis == Basis.LIVE
    assert negotiated_formula_live.head_count == 0
    assert isnan(negotiated_formula_live.avg_price)
    assert isnan(negotiated_formula_live.low_price)
    assert isnan(negotiated_formula_live.high_price)


def test_record_array():
    records = to_array([negotiated, negotiated_formula, market_formula, negotiated_live, negotiated_formula_live])
    assert len(records) == 5
    assert all(records.date == date(2019, 1, 31))
