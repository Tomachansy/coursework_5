import json
from typing import Union
import os

import marshmallow
import marshmallow_dataclass

from game.equipment import EquipmentData

BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))
EQUIPMENT_PATH: str = os.path.join(BASE_DIR, 'data', 'equipment.json')


def read_json(file_path: str, encoding: str = 'utf-8') -> Union[dict, list]:
    try:
        with open(file_path, encoding=encoding) as f:
            return json.load(f)
    except Exception:
        raise ValueError


def get_equipment_data() -> EquipmentData:
    """
    Загрузка json в переменную EquipmentData
    """
    equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
    try:
        return equipment_schema().load(data=read_json(EQUIPMENT_PATH))
    except marshmallow.exceptions.ValidationError:
        raise ValueError
