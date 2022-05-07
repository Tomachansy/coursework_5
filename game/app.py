from functools import wraps
from typing import Dict

from flask import Flask, render_template, request, redirect, url_for

from equipment import EquipmentData
from utils import get_equipment_data
from personages import personage_classes
from hero import Player, Enemy, Hero
from controller import Game

app = Flask(__name__)
app.url_map.strict_slashes = False

heroes: Dict[str, Hero] = dict()

EQUIPMENT: EquipmentData = get_equipment_data()

game = Game()


def game_processing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if game.game_is_running:
            return func(*args, **kwargs)
        if game.battle_result:
            return render_template('fight.html', heroes=heroes, result=game.battle_result)
        return redirect(url_for('menu_page'))

    return wrapper


def render_choose_personage_template(*args, **kwargs) -> str:
    return render_template(
        'hero_choosing.html',
        result={
            'classes': personage_classes,
            'weapons': EQUIPMENT.get_weapons_names,
            'armors': EQUIPMENT.get_armors_names,
            **kwargs
        }
    )


@app.route("/")
def menu_page():
    """ Заглавная страница """
    return render_template('index.html')


@app.route("/choose-hero/", methods=['GET', 'POST'])
def choose_hero():
    """ Выбор персонажа игроком """
    if request.method == 'GET':
        return render_choose_personage_template(
            result={'header': 'Выберите героя'}
        )
    heroes['player'] = \
        Player(name=request.form['name'],
               unit_class=personage_classes.get(request.form['unit_class']),
               weapon=EQUIPMENT.get_weapon(request.form['weapon']),
               armor=EQUIPMENT.get_armor(request.form['armor'])
               )
    return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['GET', 'POST'])
def choose_enemy():
    """ Выбор противника игроком"""
    if request.method == 'GET':
        return render_choose_personage_template(
            result={'header': 'Выберите врага'}
        )
    heroes['enemy'] = \
        Enemy(name=request.form['name'],
              unit_class=personage_classes[request.form['unit_class']],
              weapon=EQUIPMENT.get_weapon(request.form['weapon']),
              armor=EQUIPMENT.get_armor(request.form['armor'])
              )
    return redirect(url_for('start_fight'))


@app.route("/fight/")
def start_fight():
    """ Экран боя """
    if 'player' in heroes and 'enemy' in heroes:
        game.start_game(**heroes)
        return render_template('fight.html', heroes=heroes, result='Начинаем бой!')
    return redirect(url_for('menu_page'))


@app.route("/fight/hit")
@game_processing
def hit():
    """ Нанесение удара и обновление экрана боя """
    return render_template('fight.html', heroes=heroes, result=game.player_hit())


@app.route("/fight/use-skill")
@game_processing
def use_skill():
    """ Использование умения и обновление экрана боя """
    return render_template('fight.html', heroes=heroes, result=game.player_use_skill())


@app.route("/fight/pass-turn")
@game_processing
def pass_turn():
    """ Пропуск хода и обновление экрана боя """
    return render_template('fight.html', heroes=heroes, result=game.next_turn())


@app.route("/fight/end-fight")
def end_fight():
    """ Завершение игры и переход на заглавную страницу """
    return redirect(url_for('menu_page'))


if __name__ == "__main__":
    app.run()
