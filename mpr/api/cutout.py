from enum import Enum
from typing import Iterator
from datetime import date
from datetime import datetime

from numpy import float32
from numpy import datetime64

from ..model.cutout import Cutout
from . import Attributes
from . import Report
from . import fetch
from . import filter_sections

date_format = "%m/%d/%Y"


class Section(Enum):
    CUTOUT = 'Cutout and Primal Values'
    # DAILY_CHANGE = 'Change From Prior Day'
    # FIVE_DAY_AVERAGE = '5-Day Average Cutout and Primal Values'
    VOLUME = 'Current Volume'
    # LOIN = 'Loin Cuts'
    # BUTT = 'Butt Cuts'
    # PICNIC = 'Picnic Cuts'
    # HAM = 'Ham Cuts'
    # BELLY = 'Belly Cuts'
    # RIB = 'Sparerib Cuts'
    # JOWL = 'Jowl Cuts'
    # TRIM = 'Trim Cuts'
    # VARIETY = 'Variety Cuts'
    # ADDED_INGREDIENT = 'Added Ingredient Cuts'


def parse_attributes(cutout: Attributes, volume: Attributes) -> Cutout:
    report_date_string = cutout['report_date']
    report_date = datetime64(datetime.strptime(report_date_string, date_format).date(), 'D')

    return Cutout(
        date=report_date,
        report_date=report_date,
        primal_loads=float32(volume['temp_cuts_total_load']),
        trimming_loads=float32(volume['temp_process_total_load']),
        carcass_price=float32(cutout['pork_carcass']),
        loin_price=float32(cutout['pork_loin']),
        butt_price=float32(cutout['pork_butt']),
        picnic_price=float32(cutout['pork_picnic']),
        rib_price=float32(cutout['pork_rib']),
        ham_price=float32(cutout['pork_ham']),
        belly_price=float32(cutout['pork_belly']))


async def fetch_cutout(report: Report, start_date: date, end_date=date.today()) -> Iterator[Cutout]:
    response = await fetch(report, start_date, end_date)

    return map(lambda it: parse_attributes(*it),
            filter_sections(response, Section.VOLUME.value, Section.CUTOUT.value))


async def morning(start_date: date, end_date=date.today()) -> Iterator[Cutout]:
    return await fetch_cutout(Report.CUTOUT_MORNING, start_date, end_date)


async def afternoon(start_date: date, end_date=date.today()) -> Iterator[Cutout]:
    return await fetch_cutout(Report.CUTOUT_AFTERNOON, start_date, end_date)


lm_pk600 = pk600 = morning
lm_pk602 = pk602 = afternoon