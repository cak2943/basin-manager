"""HMS Basin Manager - Tools for managing HEC-HMS basin and pdata files"""

# Import main classes for convenient access
from .basins import (
    BasinFile,
    BasinObject,
    Basin,
    Subbasin,
    Reach,
    Junction,
    Diversion,
    Reservoir,
    Source,
    ObjectType,
    GenericFile,
)

from .hms_file_object import HMSFileObject

from .pdata import (
    PdataFile,
    PdataTable,
    PondTable,
    ReservoirTable,
    DiverSionTable,
)

__all__ = [
    "BasinFile",
    "BasinObject",
    "Basin",
    "Subbasin",
    "Reach",
    "Junction",
    "Diversion",
    "Reservoir",
    "Source",
    "ObjectType",
    "HMSFileObject",
    "GenericFile",
    "PdataFile",
    "PdataTable",
    "PondTable",
    "ReservoirTable",
    "DiverSionTable",
]


def hello() -> str:
    return "Hello from basin-manager!"
