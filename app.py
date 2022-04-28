from flask import Flask, render_template
from services.create_data import create_data
from db_config import db

# Blueprints
from views.choose_hero import choose_hero_view
from views.fight import fight_view


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(choose_hero_view, url_prefix='/choose-hero')
app.register_blueprint(fight_view, url_prefix='/fight')


@app.route('/', endpoint='main')
def main():
    create_data(app, db)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
