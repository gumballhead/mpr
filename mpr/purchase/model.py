from typing import NamedTuple
from typing import Iterator

import numpy as np
from numpy import uint8
from numpy import uint32
from numpy import float32
from numpy import recarray

from mpr.date import date_type
from mpr.date import Date
from mpr.date import to_ordinal


class Purchase(NamedTuple):
    date: Date
    report_date: Date
    seller: uint8
    arrangement: uint8
    basis: uint8
    head_count: uint32
    avg_price: float32
    low_price: float32
    high_price: float32

    def __hash__(self) -> int:
        return hash((
            to_ordinal(self.date),
            to_ordinal(self.report_date),
            self.seller,
            self.arrangement,
            self.basis))

    def __eq__(self, other) -> bool:
        return isinstance(other, Purchase) and hash(self) == hash(other) and np.allclose(self[5:], other[5:])


def to_array(records: Iterator[Purchase]) -> recarray:
    return np.rec.array(list(records), dtype=np.dtype([
        ('date', date_type),
        ('report_date', date_type),
        ('seller', uint8),
        ('arrangement', uint8),
        ('basis', uint8),
        ('head_count', uint32),
        ('avg_price', float32),
        ('low_price', float32),
        ('high_price', float32)
    ]))
