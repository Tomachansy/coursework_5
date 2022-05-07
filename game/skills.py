from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Skill(ABC):
    """
    Базовый класс умения
    """
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass


class FerociousKick(Skill):
    name = "Свирепый пинок"
    stamina = 6
    damage = 12


class PowerfulStab(Skill):
    name = "Мощный укол"
    stamina = 5
    damage = 15
