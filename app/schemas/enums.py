from enum import Enum


class BasicEnum(str, Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class BuildingConditionEnum(BasicEnum):
    intact = "Неушкоджена"
    damaged = "Пошкоджена"
    none = "Зруйнована"


class ElectricityEnum(BasicEnum):
    stable = "Стабільна"
    intermittent = "Переривчаста"
    no_data = "Відсутня"


class CarEntranceEnum(BasicEnum):
    accessible = "Доступне"
    inaccessible = "Недоступне"
    no_data = "Інформація відсутня"


class WaterEnum(BasicEnum):
    stable = "Стабільна"
    unstable = "Нестабільна"
    no_data = "Інформація відсутня"


class FuelStationEnum(BasicEnum):
    open = "Відчинено"
    closed = "Зачинено"
    no_data = "Інформація відсутня"


class HospitalEnum(BasicEnum):
    open = "Відчинено"
    closed = "Зачинено"
    no_data = "Інформація відсутня"
