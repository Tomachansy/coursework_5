from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint
from typing import Optional

from game.equipment import Weapon, Armor
from game.personages import Personage

STAMINA_PER_ROUND = 1


class Hero(ABC):
    """
    Базовый класс персонажа
    """
    def __init__(self, name: str, unit_class: Personage, weapon: Weapon, armor: Armor):
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self._is_skill_used: bool = False

    @property
    def health_points(self) -> float:
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        return round(self.stamina, 1)

    @property
    def skill_name(self) -> str:
        return self.unit_class.skill.name

    @property
    def _total_armor(self):
        """
        Расчет брони цели
        """
        if self.stamina - self.armor.stamina_per_turn >= 0:
            return self.armor.defence * self.unit_class.armor
        return 0

    def _hit(self, target: Hero) -> Optional[float]:
        """
        Логика расчета урона и уменьшение выносливости
        """
        if self.stamina - self.weapon.stamina_per_hit < 0:
            return None
        hero_damage = self.weapon.damage * self.unit_class.attack  # расчет урона атакующего
        dealt_damage = hero_damage - target._total_armor  # расчет урона
        if dealt_damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit
        return round(dealt_damage, 1)

    def take_hit(self, damage: float):
        if damage > 0:
            self.hp -= damage
            self.hp = self.hp
            return round(damage, 1)
        return None

    def regenerate_stamina(self) -> None:
        """
        Регенерация выносливости для игрока и врага за ход
        """
        delta_stamina = STAMINA_PER_ROUND * self.unit_class.stamina
        if self.stamina + delta_stamina <= self.unit_class.max_stamina:
            self.stamina += delta_stamina
        else:
            self.stamina = self.unit_class.max_stamina

    def use_skill(self) -> Optional[float]:
        """
        Метод использования умения
        """
        if self._is_skill_used:
            return True
        if not self._is_skill_used and self.stamina - self.unit_class.skill.stamina:
            self._is_skill_used = True
            return round(self.unit_class.skill.damage, 1)
        return None

    @abstractmethod
    def hit(self, target: Hero) -> Optional[float]:
        pass


class Player(Hero):

    def hit(self, target: Hero) -> Optional[float]:
        """
        Функция удар игрока
        """
        result = self._hit(target)
        return result


class Enemy(Hero):

    def hit(self, target: Hero) -> str | float | None:
        """
        Функция удар соперника и 10% шанс применения умения
        """
        if randint(0, 100) < 10 and self.stamina >= self.unit_class.skill.stamina and not self._is_skill_used:
            return "use skill"

        result = self._hit(target)
        return result



