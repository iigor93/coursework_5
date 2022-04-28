from db_config import db
from models.classes import Unit
from models.equipments import Weapon, Armor
from random import randint


class PlayerUnit(db.Model):
    __tablename__ = 'player_unit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    health_points = db.Column(db.Float)
    stamina_points = db.Column(db.Float)
    unit_class = db.relationship('Unit')
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    weapon = db.relationship('Weapon')
    weapon_id = db.Column(db.Integer, db.ForeignKey('weapon.id'))
    armor = db.relationship('Armor')
    armor_id = db.Column(db.Integer, db.ForeignKey('armor.id'))

    def stamina_skill(self, stamina_increase):
        """Проверка достаточно ли выносливости для использования умения"""
        if self.stamina_points >= self.unit_class.skill.stamina_required:
            new_stamina = self.stamina_points - self.unit_class.skill.stamina_required + \
                                  (stamina_increase * self.unit_class.stamina_modifier)
            if new_stamina > self.unit_class.max_stamina:
                self.stamina_points = self.unit_class.max_stamina
            else:
                self.stamina_points = round(new_stamina, 1)
            return True
        return False

    def stamina_weapon(self, stamina_increase):
        """Проверка достаточно ли выносливости для использования оружия"""
        if self.stamina_points >= self.weapon.stamina_per_hit:
            new_stamina = self.stamina_points - self.weapon.stamina_per_hit + \
                                  (stamina_increase * self.unit_class.stamina_modifier)
            if new_stamina > self.unit_class.max_stamina:
                self.stamina_points = self.unit_class.max_stamina
            else:
                self.stamina_points = round(new_stamina, 1)
            return True
        new_stamina = self.stamina_points + (stamina_increase * self.unit_class.stamina_modifier)
        if new_stamina > self.unit_class.max_stamina:
            self.stamina_points = self.unit_class.max_stamina
        else:
            self.stamina_points = round(new_stamina, 1)
        return False

    def stamina_armor(self, stamina_increase):
        """Проверка достаточно ли выносливости для использования защиты"""
        if self.stamina_points >= self.armor.stamina_per_turn:
            new_stamina = self.stamina_points - self.armor.stamina_per_turn + \
                                  (stamina_increase * self.unit_class.stamina_modifier)
            if new_stamina > self.unit_class.max_stamina:
                self.stamina_points = self.unit_class.max_stamina
            else:
                self.stamina_points = round(new_stamina, 1)
            return True
        new_stamina = self.stamina_points + (stamina_increase * self.unit_class.stamina_modifier)
        if new_stamina > self.unit_class.max_stamina:
            self.stamina_points = self.unit_class.max_stamina
        else:
            self.stamina_points = round(new_stamina, 1)
        return False

    def hit(self, stamina_increase):
        """Вычисление урона при ударе"""
        if self.stamina_weapon(stamina_increase):
            weapon_damage = self.weapon.get_damage()
            return weapon_damage * self.unit_class.attack_modifier
        return False

    def armor_func(self, stamina_increase):
        """Вычисление уровня защиты"""
        if self.stamina_armor(stamina_increase):
            return self.armor.defence * self.unit_class.armor_modifier
        return 0
