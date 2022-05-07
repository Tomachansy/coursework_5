from abc import ABC
from dataclasses import dataclass

from game.skills import Skill, FerociousKick, PowerfulStab


@dataclass
class Personage(ABC):
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


Warrior = Personage(
    name="Воин",
    max_health=60.0,
    max_stamina=30.0,
    attack=0.8,
    stamina=0.9,
    armor=1.2,
    skill=FerociousKick()
)


Thief = Personage(
    name="Вор",
    max_health=50.0,
    max_stamina=25.0,
    attack=1.5,
    stamina=1.2,
    armor=1.0,
    skill=PowerfulStab()
)


personage_classes: dict[str, Personage] = {
    Thief.name: Thief,
    Warrior.name: Warrior
}
