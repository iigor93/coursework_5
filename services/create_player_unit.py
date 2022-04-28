from models.units import PlayerUnit
from models.arena_class import Arena
from db_config import db
from models.classes import Unit
from models.equipments import Weapon, Armor


def create_player_unit(data_received):
    """Создание персонажей из данных введенных на странице"""
    name = data_received.get('name')
    type_ = data_received.get('type')
    unit_class = data_received.get('unit_class')
    unit_obj = db.session.query(Unit).filter_by(name=unit_class).one()
    weapon = data_received.get('weapon')
    weapon_obj = db.session.query(Weapon).filter_by(name=weapon).one()
    armor = data_received.get('armor')
    armor_obj = db.session.query(Armor).filter_by(name=armor).one()

    health_points = unit_obj.max_health
    stamina_points = unit_obj.max_stamina

    player_unit = PlayerUnit(name=name, weapon_id=weapon_obj.id, armor_id=armor_obj.id, unit_id=unit_obj.id,
                             type=type_, health_points=health_points, stamina_points=stamina_points)

    db.session.add(player_unit)
    db.session.commit()


def create_arena():
    """Создание арены"""
    player = db.session.query(PlayerUnit).filter_by(type='user').first()
    enemy = db.session.query(PlayerUnit).filter_by(type='enemy').first()

    arena = Arena(player_id=player.id, enemy_id=enemy.id)
    db.session.add(arena)
    db.session.commit()
