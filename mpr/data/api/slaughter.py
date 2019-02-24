from enum import Enum
from typing import Iterator
from datetime import date
from datetime import datetime
from datetime import timedelta
from functools import singledispatch

from numpy import datetime64

from mpr.data.model.slaughter import Slaughter
from mpr.data.model.purchase_type import Seller, Arrangement, Basis

from . import Attributes
from . import Report
from . import opt_int
from . import opt_float
from . import date_interval
from . import fetch
from . import filter_section

date_format = "%m/%d/%Y"


class Section(Enum):
    # SUMMARY = 'Summary'
    BARROWS_AND_GILTS = 'Barrows/Gilts'
    # CARCASS_MEASUREMENTS = 'Carcass Measurements'
    # SOWS_AND_BOARS = 'Sows/Boars'
    # SCHEDULED_SWINE = '14-Day Scheduled Swine'
    # NEGOTIATED_BARROWS_AND_GILTS = 'Barrows/Gilts Negotiated'


purchase_types = {
    'Prod. Sold Negotiated':
        (Seller.PRODUCER, Arrangement.NEGOTIATED, Basis.ALL),

    'Prod. Sold Swine or Pork Market Formula':
        (Seller.PRODUCER, Arrangement.MARKET_FORMULA, Basis.ALL),

    'Prod. Sold Other Market Formula':
        (Seller.PRODUCER, Arrangement.OTHER_MARKET_FORMULA, Basis.ALL),

    'Prod. Sold Negotiated Formula':
        (Seller.PRODUCER, Arrangement.NEGOTIATED_FORMULA, Basis.ALL),

    'Prod. Sold Other Purchase Arrangement':
        (Seller.PRODUCER, Arrangement.OTHER_PURCHASE, Basis.ALL),

    'Prod. Sold (All Purchase Types)':
        (Seller.PRODUCER, Arrangement.ALL, Basis.ALL),

    'Pack. Sold (All Purchase Types)':
        (Seller.PACKER, Arrangement.ALL, Basis.ALL),

    'Packer Owned':
        (Seller.PACKER, Arrangement.PACKER_OWNED, Basis.ALL)
}


def parse_attributes(attr: Attributes) -> Slaughter:
    report_date = datetime.strptime(attr['for_date_begin'], date_format).date()
    purchase_type = attr['purchase_type']
    (seller, arrangement, basis) = purchase_types[purchase_type]

    return Slaughter(
        date=datetime64(report_date, 'D'),
        seller=seller.value,
        arrangement=arrangement.value,
        basis=basis.value,
        head_count=opt_int(attr, 'head_count'),
        base_price=opt_float(attr, 'base_price'),
        net_price=opt_float(attr, 'avg_net_price'),
        low_price=opt_float(attr, 'lowest_net_price'),
        high_price=opt_float(attr, 'highest_net_price'),
        live_weight=opt_float(attr, 'avg_live_weight'),
        carcass_weight=opt_float(attr, 'avg_carcass_weight'),
        sort_loss=opt_float(attr, 'avg_sort_loss'),
        backfat=opt_float(attr, 'avg_backfat'),
        loin_depth=opt_float(attr, 'avg_loin_depth'),
        loineye_area=opt_float(attr, 'loineye_area'),
        lean_percent=opt_float(attr, 'avg_lean_percent'))


@singledispatch
async def fetch_slaughter(start_date: date, end_date=date.today()) -> Iterator[Slaughter]:
    response = await fetch(Report.SLAUGHTERED_SWINE, start_date + timedelta(days=1), end_date)
    return map(parse_attributes, filter_section(response, Section.BARROWS_AND_GILTS.value))


@fetch_slaughter.register(int)
async def fetch_slaughter_days(days: int) -> Iterator[Slaughter]:
    return await fetch_slaughter(*date_interval(days))


lm_hg201 = hg201 = fetch_slaughter
