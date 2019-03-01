from typing import Iterator

import pandas as pd
from pandas import Series
from pandas import DataFrame

from mpr.data.model.cutout import Cutout
from mpr.data.model.cutout import to_array

from .. import create_table
from .. import with_change


def cutout_index(loads: Series, carcass_price: Series) -> Series:
    values = loads * carcass_price
    pivot_table = pd.pivot_table(pd.concat([loads.rename('loads'), values.rename('value')], axis=1), index='date')
    rolling_totals = pivot_table.rolling(5).sum().dropna()

    return rolling_totals.value / rolling_totals.loads


def cutout_report(records: Iterator[Cutout]) -> DataFrame:
    array = to_array(records)
    data = DataFrame(array).set_index('date').sort_values(by='date')

    loads = data.primal_loads + data.trimming_loads
    carcass_price, price_change = with_change(data.carcass_price)
    index, index_change = with_change(cutout_index(loads, carcass_price))

    return create_table(
        index.rename('Cutout Index'),
        index_change.rename('Index Change'),
        carcass_price.rename('Carcass Price'),
        price_change.rename('Price Change'),
        loads.rename('Total Loads'),
        data.loin_price.rename('Loin Price'),
        data.belly_price.rename('Belly Price'),
        data.belly_price.rename('Butt Price'),
        data.ham_price.rename('Ham Price'),
        data.rib_price.rename('Rib Price'),
        data.picnic_price.rename('Picnic Price'))