# SkyWars
https://hub.docker.com/repository/docker/chickyd0t/skywars

Игра с веб-интерфейсом, битва героев в стиле олдскульных браузерных игр.  
#### Выбор:
- класс персонажей: Воин (умение - "Свирепый пинок"), Вор (умение - "Мощный укол")
- оружие: топорик, ножик, ладошки
- броня: футболка, кожаная броня, панцирь

#### Данные о персонаже:
- очки здоровья
- очки выносливости

#### Исход битвы:
- Игрок победил.
- Игрок проиграл.
- Ничья.
#
### Механика боя

Бой состоит из ходов. В течение 1 хода игрок может нанести удар, воспользоваться умением или пропустить ход.

Каждый новый ход выносливости игроков увеличивается на 3 ед. (Не может превышать максимальное значение.)

Бой происходит с компьютерным противником. После действия игрока компьютер отвечает тем же. 

Как игрок, так и компьютер могут использовать умение только один раз за бой.

Когда компьютер выполняет ответное действие, он имеет 10%-ный шанс воспользоваться умением. Если шанс срабатывает, а умение уже было применено, то компьютер наносит обычный удар.

Битва окончена, если у одного из персонажей очки здоровья меньше нуля.