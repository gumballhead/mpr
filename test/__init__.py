from typing import Iterator
from typing import TextIO
from xml.etree import ElementTree

from mpr.api import Attributes
from mpr.api import parse_elements


def parse_report(report: TextIO) -> Iterator[Attributes]:
    elements = ElementTree.iterparse(report, events=['start', 'end'])
    return parse_elements(elements)


def load_resource(name: str) -> Iterator[Attributes]:
    with open(f"test/resources/{name}") as report:
        for element in parse_report(report):
            yield element
