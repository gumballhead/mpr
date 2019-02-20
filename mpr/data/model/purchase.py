from abc import ABC
from typing import Optional
from dataclasses import dataclass
from datetime import date

from tables import UInt32Col
from tables import Float32Col
from tables.tableextension import Row

from .observation import Observation
from .purchase_type import Seller
from .purchase_type import Arrangement
from .purchase_type import Basis
from .purchase_type import PurchaseTypeCol


@dataclass
class Purchase(Observation, ABC):
    date: date
    seller: Seller
    arrangement: Arrangement
    basis: Basis
    head_count: int
    avg_price: Optional[float]
    low_price: Optional[float]
    high_price: Optional[float]

    schema = {
        'date': UInt32Col(),
        'purchase_type': PurchaseTypeCol(),
        'head_count': UInt32Col(),
        'avg_price': Float32Col(),
        'low_price': Float32Col(),
        'high_price': Float32Col()
    }

    @classmethod
    def from_row(cls, row: Row) -> 'Purchase':
        return cls(
            date=date.fromordinal(row['date']),
            seller=Seller.from_ordinal(row['purchase_type/seller']),
            arrangement=Arrangement.from_ordinal(row['purchase_type/arrangement']),
            basis=Basis.from_ordinal(row['purchase_type/basis']),
            head_count=row['head_count'],
            avg_price=row['avg_price'],
            low_price=row['low_price'],
            high_price=row['high_price'])

    def append(self):
        row = self.table.row

        row['date'] = self.date.toordinal()
        row['purchase_type/seller'] = self.seller.to_ordinal()
        row['purchase_type/arrangement'] = self.arrangement.to_ordinal()
        row['purchase_type/basis'] = self.basis.to_ordinal()
        row['head_count'] = self.head_count
        row['avg_price'] = self.avg_price
        row['low_price'] = self.low_price
        row['high_price'] = self.high_price

        row.append()
