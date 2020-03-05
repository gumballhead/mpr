from typing import NamedTuple
from typing import Iterator

from numpy import float32
from numpy import recarray
from numpy import allclose
from numpy import dtype
from numpy import rec

from ..date import Date
from ..date import date64
from ..date import to_ordinal


class Cutout(NamedTuple):
    date: Date
    report_date: Date
    primal_loads: float32
    trimming_loads: float32
    carcass_price: float32
    loin_price: float32
    butt_price: float32
    picnic_price: float32
    rib_price: float32
    ham_price: float32
    belly_price: float32

    def __hash__(self) -> int:
        return hash((to_ordinal(self.date), to_ordinal(self.report_date)))

    def __eq__(self, other) -> bool:
        return (isinstance(other, Cutout) and hash(self) == hash(other) and
            allclose(self[2:], other[2:], equal_nan=True))

    @property
    def loads(self) -> int:
        return self.primal_loads + self.trimming_loads

    @property
    def value(self) -> float:
        return self.loads * self.carcass_price


def to_array(records: Iterator[Cutout]) -> recarray:
    return rec.array(list(records), dtype=dtype([
        ('date', date64),
        ('report_date', date64),
        ('primal_loads', float32),
        ('trimming_loads', float32),
        ('carcass_price', float32),
        ('loin_price', float32),
        ('butt_price', float32),
        ('picnic_price', float32),
        ('rib_price', float32),
        ('ham_price', float32),
        ('belly_price', float32)
    ]))
