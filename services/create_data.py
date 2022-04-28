from models.classes import Skill, Unit
from models.equipments import Weapon, Armor
import json


with open('data/equipment.json', 'r', encoding='utf8') as f:
    file_read = json.load(f)


def create_data(app, db):
    """ Наполняем БД данными """
    with app.app_context():
        db.drop_all()
        db.create_all()

        skill_one = Skill(id=1, name='Свирепый пинок', damage=12, stamina_required=6)
        skill_two = Skill(id=2, name='Мощный укол', damage=15, stamina_required=5)
        db.session.add_all([skill_one, skill_two])

        warrior = Unit(name='Воин', max_health=60.0, max_stamina=30.0,
                       attack_modifier=0.8, stamina_modifier=0.9, armor_modifier=1.2,
                       skill_id=1)

        thief = Unit(name='Вор', max_health=50.0, max_stamina=25.0,
                     attack_modifier=1.2, stamina_modifier=1.1, armor_modifier=1.0,
                     skill_id=2)

        db.session.add_all([warrior, thief])

        weapons_list = file_read.get('weapons')
        temp_list_w = []
        for item in weapons_list:
            weapon_temp = Weapon(**item)
            temp_list_w.append(weapon_temp)

        db.session.add_all(temp_list_w)

        armor_list = file_read.get('armors')
        temp_list_a = []
        for item in armor_list:
            armor_temp = Armor(**item)
            temp_list_a.append(armor_temp)

        db.session.add_all(temp_list_a)

        db.session.commit()
