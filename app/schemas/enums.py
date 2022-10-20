from enum import Enum


class BasicEnum(str, Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class BuildingConditionEnum(BasicEnum):
    intact = "Неушкоджена"
    damaged = "Пошкоджена"
    none = "Невідомо"


class ElectricityEnum(BasicEnum):
    stable = "Стабільна"
    intermittent = "Переривчаста"
    no_data = "Невідомо"


class CarEntranceEnum(BasicEnum):
    accessible = "Доступне"
    inaccessible = "Недоступне"
    no_data = "Невідомо"


class WaterEnum(BasicEnum):
    stable = "Стабільна"
    unstable = "Нестабільна"
    no_data = "Невідомо"


class FuelStationEnum(BasicEnum):
    open = "Відчинено"
    closed = "Зачинено"
    no_data = "Невідомо"


class HospitalEnum(BasicEnum):
    open = "Відчинено"
    closed = "Зачинено"
    no_data = "Невідомо"
