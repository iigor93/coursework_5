from db_config import db


class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    damage = db.Column(db.Float)
    stamina_required = db.Column(db.Float)
    was_used = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.name


class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    max_health = db.Column(db.Float)
    max_stamina = db.Column(db.Float)
    attack_modifier = db.Column(db.Float)
    stamina_modifier = db.Column(db.Float)
    armor_modifier = db.Column(db.Float)
    skill = db.relationship('Skill')
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))

    def __repr__(self):
        return self.name
