from typing import Optional

from hero import Hero


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Game(metaclass=BaseSingleton):

    def __init__(self):
        self.player = None
        self.enemy = None
        self.game_is_running = False
        self.battle_result = ''

    def start_game(self, player: Hero, enemy: Hero) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_hp(self) -> Optional[str]:
        """
        Проверка здоровья игрока и врага и возвращение результата строкой
        """
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            return self._end_game(result="Ничья!")
        if self.enemy.hp <= 0:
            return self._end_game(result="Игрок победил!")
        if self.player.hp <= 0:
            return self._end_game(result="Игрок проиграл!")

        return None

    def _end_game(self, result: str) -> str:
        self._instances = {}
        self.game_is_running = False
        self.battle_result = result

        return result

    def next_turn(self) -> str:
        """
        Функция следующего хода при пропуске хода или нанесения удара
        """
        if result := self._check_hp():
            return result

        if not self.game_is_running:
            return self.battle_result

        result = self.enemy_hit()
        self._stamina_regenerate()
        return result

    def _stamina_regenerate(self):
        self.player.regenerate_stamina()
        self.enemy.regenerate_stamina()

    def enemy_hit(self) -> str:
        """
        Удар противника и возвращение результата строкой
        """
        dealt_damage = self.enemy.hit(self.player)
        if dealt_damage == "use skill":
            return self.enemy_use_skill()
        elif dealt_damage is not [None, str]:
            if dealt_damage is not 0:
                self.player.take_hit(dealt_damage)
                return f"{self.enemy.name.title()} используя {self.enemy.weapon.name} пробивает " \
                       f"{self.player.armor.name} и наносит {dealt_damage} урона.\n"
            else:
                return f"{self.enemy.name.title()} используя {self.enemy.weapon.name} наносит удар, " \
                       f"но {self.player.armor.name} его останавливает.\n"
        else:
            return f"{self.enemy.name.title()} попытался использовать {self.enemy.weapon.name}, " \
                   f"но у него не хватило выносливости.\n"

    def enemy_use_skill(self) -> str:
        """
        Использование умения противником
        """
        dealt_damage: Optional[float] = self.enemy.use_skill()
        if dealt_damage is True:
            return f'Навык уже использован.\n'
        if dealt_damage is not [None, True]:
            self.enemy.take_hit(dealt_damage)
            return f"{self.enemy.name.title()} использует {self.enemy.skill_name} и наносит " \
                   f"{dealt_damage} урона сопернику.\n"
        return f"{self.enemy.name.title()} попытался использовать {self.enemy.skill_name} " \
               f"но у него не хватило выносливости.\n"

    def player_hit(self) -> str:
        """
        Удар игрока и возвращение результата строкой
        """
        dealt_damage: Optional[float] = self.player.hit(self.enemy)
        if dealt_damage is not None:
            if dealt_damage is not 0:
                self.enemy.take_hit(dealt_damage)
                return f"{self.player.name.title()} используя {self.player.weapon.name} пробивает " \
                       f"{self.enemy.armor.name} и наносит {dealt_damage} урона.\n{self.next_turn()}"
            return f"{self.player.name.title()} используя {self.player.weapon.name} наносит удар, " \
                   f"но {self.enemy.armor.name} его останавливает.\n{self.next_turn()}"
        return f"{self.player.name.title()} попытался использовать {self.player.weapon.name}, " \
               f"но у него не хватило выносливости.\n{self.next_turn()}"

    def player_use_skill(self) -> str:
        """
        Использование умения игроком
        """
        dealt_damage: Optional[float] = self.player.use_skill()
        if dealt_damage is True:
            return f'Навык уже использован.\n'
        if dealt_damage is not [None, True]:
            self.enemy.take_hit(dealt_damage)
            return f"{self.player.name.title()} использует {self.player.skill_name} и наносит " \
                   f"{dealt_damage} урона сопернику.\n{self.next_turn()}"
        return f"{self.player.name.title()} попытался использовать {self.player.skill_name}, " \
               f"но у него не хватило выносливости.\n{self.next_turn()}"
