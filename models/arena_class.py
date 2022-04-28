from db_config import db
from models.classes import Unit
from models.equipments import Weapon, Armor
from random import randint


class Arena(db.Model):
    __tablename__ = 'arena'
    id = db.Column(db.Integer, primary_key=True)
    player = db.relationship('PlayerUnit', foreign_keys='Arena.player_id')
    player_id = db.Column(db.Integer, db.ForeignKey('player_unit.id'))
    enemy = db.relationship('PlayerUnit', foreign_keys='Arena.enemy_id')
    enemy_id = db.Column(db.Integer, db.ForeignKey('player_unit.id'))
    stamina_increase = db.Column(db.Integer, default=1)
    comment = db.Column(db.String, default='')
    winner = db.Column(db.String, default='')

    def win(self):
        """Проверка победителя"""
        if self.player.health_points < 0 and self.enemy.health_points >= 0:
            self.winner = f'Победитель {self.enemy.name}'
            return True
        elif self.player.health_points >= 0 and self.enemy.health_points < 0:
            self.winner = f'Победитель {self.player.name}'
            return True
        elif self.player.health_points < 0 and self.enemy.health_points < 0:
            self.winner = f'Ничья'
            return True
        return False

    def player_hit(self):
        """Удар игрока"""
        weapon_damage = self.player.hit(self.stamina_increase)
        if weapon_damage is False:
            self.comment = f"{self.player.name} - Не достаточно выносливости для удара.   "
            return False
        armor_defence = self.enemy.armor_func(self.stamina_increase)
        if armor_defence <= weapon_damage:
            final_damage = round(weapon_damage - armor_defence, 1)
            self.enemy.health_points = round(self.enemy.health_points - final_damage, 1)
            self.comment = f'{self.player.name}, используя {self.player.weapon.name}, пробивает ' \
                           f'{self.enemy.armor.name} соперника и наносит {final_damage} урона.    '
        else:
            self.comment = f"{self.player.name}, используя {self.player.weapon.name}, наносит удар, " \
                          f"но {self.enemy.armor.name} соперника его останавливает.   "
            return False

    def enemy_hit(self):
        """Удар соперника"""
        if self.enemy.unit_class.skill.was_used is False and randint(1, 10) == 4:
            self.enemy.unit_class.skill.was_used = True
            if self.enemy.stamina_skill(self.stamina_increase):
                self.player.health_points -= self.enemy.unit_class.skill.damage
                self.comment += f'{self.enemy.name} использовал умение, нанес {self.enemy.unit_class.skill.damage} урона'
            else:
                self.comment += 'Не достаточно выносливости для умения.   '
        else:
            weapon_damage = self.enemy.hit(self.stamina_increase)
            if weapon_damage is False:
                self.comment += f" {self.enemy.name} - Не достаточно выносливости для удара"
                return False
            armor_defence = self.player.armor_func(self.stamina_increase)
            if armor_defence <= weapon_damage:
                final_damage = round(weapon_damage - armor_defence, 1)
                self.player.health_points = round(self.player.health_points - final_damage, 1)
                self.comment += f'{self.enemy.name}, используя {self.enemy.weapon.name}, пробивает ' \
                                f'{self.player.armor.name} соперника и наносит {final_damage} урона.'
            else:
                self.comment += f"{self.enemy.name}, используя {self.enemy.weapon.name}, наносит удар, " \
                               f"но {self.player.armor.name} соперника его останавливает."
                return False

    def player_pass(self):
        """Пропуск игроком хода"""
        self.comment = f"{self.player.name} пропускает удар.   "

    def player_skill(self):
        """Использование умения"""
        if self.player.unit_class.skill.was_used is False:
            self.player.unit_class.skill.was_used = True
            if self.player.stamina_skill(self.stamina_increase):
                self.enemy.health_points -= self.player.unit_class.skill.damage
                self.comment = f'{self.player.name} использовал умение и нанес {self.player.unit_class.skill.damage} урона.   .'
            else:
                self.comment = 'Не достаточно выносливости для умения.   '
        else:
            self.comment = 'Умение уже было использовано.   '
