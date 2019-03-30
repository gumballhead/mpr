from typing import Dict
from typing import Iterator
from enum import Enum
from datetime import timedelta
from datetime import date

from mpr.date import from_string
from mpr.purchase.model import Purchase
from mpr.purchase_type import PurchaseType, Seller, Arrangement, Basis

from mpr.api import Attributes
from mpr.api import Report
from mpr.api import get_optional
from mpr.api import opt_int
from mpr.api import opt_float
from mpr.api import fetch
from mpr.api import filter_section

date_format = "%m/%d/%Y"


class Section(Enum):
    # VOLUME = 'Current Volume by Purchase Type'
    BARROWS_AND_GILTS = 'Barrows/Gilts (producer/packer sold)'
    # CARCASS_MEASUREMENTS = 'Matrix, 185 lb Carcass Basis'
    # CARCASS_WEIGHT_DIFF = 'Carcass Weight Differentials'
    # AVERAGE_MARKET_HOG = '5-Day Rolling Average Market Hog based on Slaughter Data Submitted'
    # SOWS = 'Sows'
    # STATES = 'State of Origin'


purchase_types: Dict[str, PurchaseType] = {
    'Negotiated (carcass basis)':
        (Seller.ALL, Arrangement.NEGOTIATED, Basis.CARCASS),

    'Negotiated Formula (carcass basis)':
        (Seller.ALL, Arrangement.NEGOTIATED_FORMULA, Basis.CARCASS),

    'Swine/Pork Market Formula (carcass basis)':
        (Seller.ALL, Arrangement.MARKET_FORMULA, Basis.CARCASS),

    'Negotiated (live basis)':
        (Seller.ALL, Arrangement.NEGOTIATED, Basis.LIVE),

    'Negotiated Formula (live basis)':
        (Seller.ALL, Arrangement.NEGOTIATED_FORMULA, Basis.LIVE),

    'Combined Negotiated/Negotiated Formula (carcass basis)':
        (Seller.ALL, Arrangement.ALL_NEGOTIATED, Basis.CARCASS),

    'Combined Negotiated/Negotiated Formula (live basis)':
        (Seller.ALL, Arrangement.ALL_NEGOTIATED, Basis.LIVE)
}


def parse_attributes(attr: Attributes) -> Purchase:
    report_date_string = attr['report_date']
    record_date_string = get_optional(attr, 'reported_for_date') or report_date_string

    purchase_type = attr['purchase_type']
    (seller, arrangement, basis) = purchase_types[purchase_type]

    return Purchase(
        date=from_string(record_date_string, date_format),
        report_date=from_string(report_date_string, date_format),
        seller=seller.value,
        arrangement=arrangement.value,
        basis=basis.value,
        head_count=opt_int(attr, 'head_count'),
        avg_price=opt_float(attr, 'wtd_avg'),
        low_price=opt_float(attr, 'price_low'),
        high_price=opt_float(attr, 'price_high'))


async def fetch_purchase(report: Report, start_date: date, end_date=date.today()) -> Iterator[Purchase]:
    response = await fetch(report, start_date, end_date)
    return map(parse_attributes, filter_section(response, Section.BARROWS_AND_GILTS.value))


async def prior_day(start_date: date, end_date=date.today()) -> Iterator[Purchase]:
    return await fetch_purchase(Report.PURCHASED_SWINE, start_date + timedelta(days=1), end_date)


async def morning(start_date: date, end_date=date.today()) -> Iterator[Purchase]:
    return await fetch_purchase(Report.DIRECT_HOG_MORNING, start_date, end_date)


async def afternoon(start_date: date, end_date=date.today()) -> Iterator[Purchase]:
    return await fetch_purchase(Report.DIRECT_HOG_AFTERNOON, start_date, end_date)


lm_hg200 = hg200 = prior_day
lm_hg202 = hg202 = morning
lm_hg203 = hg203 = afternoon
