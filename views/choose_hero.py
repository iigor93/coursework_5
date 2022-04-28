from flask import Blueprint, render_template, request, url_for, redirect
from models.classes import Unit
from services.create_player_unit import create_player_unit, create_arena
from db_config import db
from models.equipments import Weapon, Armor
from models.units import PlayerUnit


choose_hero_view = Blueprint('choose_hero', __name__)


@choose_hero_view.route('/', methods=['GET', 'POST'])
def choose_hero():
    """Выбор персонажей"""
    header = "Выберете героя"
    if request.method == 'POST':
        data_received = {'unit_class': request.values.get('unit_class'),
                         'weapon': request.values.get('weapon'),
                         'armor': request.values.get('armor'),
                         'name': request.values.get('name')
                         }

        if db.session.query(PlayerUnit).filter_by(type='user').first() is None:
            data_received['type'] = 'user'
            header = 'Выберете врага'
            create_player_unit(data_received)
        elif db.session.query(PlayerUnit).filter_by(type='enemy').first() is None:
            data_received['type'] = 'enemy'
            create_player_unit(data_received)
            create_arena()
            return redirect(url_for('fight_view.fight'))

    result = {'classes': db.session.query(Unit).all(),
              'weapons': db.session.query(Weapon).all(),
              'armors': db.session.query(Armor).all(),
              'header': header
              }

    return render_template('hero_choosing.html', result=result)
