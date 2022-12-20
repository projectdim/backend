from enum import Enum


class BasicEnum(str, Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class BuildingConditionEnum(BasicEnum):
    intact = "intact"
    damaged = "damaged"
    none = "no_data"


class ElectricityEnum(BasicEnum):
    stable = "stable"
    intermittent = "intermittent"
    no_data = "no_data"


class CarEntranceEnum(BasicEnum):
    accessible = "accessible"
    inaccessible = "inaccessible"
    no_data = "no_data"


class WaterEnum(BasicEnum):
    stable = "stable"
    unstable = "intermittent"
    no_data = "no_data"


class FuelStationEnum(BasicEnum):
    open = "open"
    closed = "closed"
    no_data = "no_data"


class HospitalEnum(BasicEnum):
    open = "open"
    closed = "closed"
    no_data = "no_data"
