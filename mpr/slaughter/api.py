from typing import Dict
from typing import Iterator
from datetime import date

from ..date import from_string
from ..purchase_type import PurchaseType, Seller, Arrangement, Basis
from ..report import lm_hg201
from ..data import opt_int
from ..data import opt_float
from ..data.api import Attributes
from ..data.repository import Repository

from .model import Slaughter

date_format = "%m/%d/%Y"


purchase_types: Dict[str, PurchaseType] = {
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
    purchase_type = attr['purchase_type']
    (seller, arrangement, basis) = purchase_types[purchase_type]

    return Slaughter(
        date=from_string(attr['for_date_begin'], date_format),
        report_date=from_string(attr['report_date'], date_format),
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


async def fetch_slaughter(start: date, end=date.today()) -> Iterator[Slaughter]:
    slaughter = await Repository(lm_hg201).query(start, end, lm_hg201.Section.BARROWS_AND_GILTS)
    return map(parse_attributes, slaughter)
