from db_config import db
from random import randint


class Weapon(db.Model):
    __tablename__ = 'weapon'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    min_damage = db.Column(db.Float)
    max_damage = db.Column(db.Float)
    stamina_per_hit = db.Column(db.Float)

    def __repr__(self):
        return self.name

    def get_damage(self):
        return randint(int(self.min_damage*10), int(self.max_damage*10))/10


class Armor(db.Model):
    __tablename__ = 'armor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    defence = db.Column(db.Float)
    stamina_per_turn = db.Column(db.Float)

    def __repr__(self):
        return self.name
