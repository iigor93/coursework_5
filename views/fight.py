from flask import Blueprint, render_template, url_for, redirect
from db_config import db
from models.arena_class import Arena
from sqlalchemy import exc

fight_view = Blueprint('fight_view', __name__)


def get_units():
    """Загрузка данных из БД"""
    arena = db.session.query(Arena).one()
    return arena


@fight_view.route('/', endpoint='fight')
def fight():
    """Основная страница битвы"""
    try:
        arena = get_units()
    except exc.OperationalError:
        return redirect(url_for('main'))
    arena.win()
    heroes = {'player': arena.player,
              'enemy': arena.enemy}
    result = arena.comment
    return render_template('fight.html', heroes=heroes, result=result, battle_result=arena.winner)


@fight_view.route('/hit')
def hit():
    """Нанесение удара"""
    try:
        arena = get_units()
    except exc.OperationalError:
        return redirect(url_for('main'))
    if arena.win() is False:
        arena.player_hit()
        arena.enemy_hit()
    db.session.add(arena)
    db.session.commit()
    return redirect(url_for('fight_view.fight'))


@fight_view.route('/use-skill')
def use_skill():
    """Использование умения"""
    try:
        arena = get_units()
    except exc.OperationalError:
        return redirect(url_for('main'))
    if arena.win() is False:
        arena.player_skill()
        arena.enemy_hit()
    db.session.add(arena.enemy)
    db.session.commit()
    return redirect(url_for('fight_view.fight'))


@fight_view.route('/pass-turn')
def pass_turn():
    """Пропуск хода"""
    try:
        arena = get_units()
    except exc.OperationalError:
        return redirect(url_for('main'))
    if arena.win() is False:
        arena.player_pass()
        arena.enemy_hit()
    db.session.add(arena)
    db.session.commit()
    return redirect(url_for('fight_view.fight'))


@fight_view.route('/end-fight')
def fight_end():
    """Завершение игры"""
    return redirect(url_for('main'))
