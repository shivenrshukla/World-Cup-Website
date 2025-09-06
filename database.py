from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------- CONFIGURE REMOTE DB HERE ----------
# Example for MySQL:
# Replace USER, PASSWORD, HOST, PORT, and DBNAME with your details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:KLLaGUreGLCRdozEPpLzIcDtwPCHtMjy@switchback.proxy.rlwy.net:37540/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------- MODELS ----------
class Player(db.Model):
    __tablename__ = 'player'
    jersey_number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    career_matches = db.Column(db.Integer)
    icc_ranking = db.Column(db.Integer)
    age = db.Column(db.Integer)


class Bowler(db.Model):
    __tablename__ = 'bowler'
    jersey_number = db.Column(db.Integer, db.ForeignKey('player.jersey_number'), primary_key=True)
    matches_played = db.Column(db.Integer)
    wickets = db.Column(db.Integer)
    economy = db.Column(db.Float)
    average = db.Column(db.Float)
    strike_rate = db.Column(db.Float)


class Batsman(db.Model):
    __tablename__ = 'batsman'
    jersey_number = db.Column(db.Integer, db.ForeignKey('player.jersey_number'), primary_key=True)
    matches_played = db.Column(db.Integer)
    runs = db.Column(db.Integer)
    highest_score = db.Column(db.Integer)
    average = db.Column(db.Float)
    strike_rate = db.Column(db.Float)


class Matches(db.Model):
    __tablename__ = 'matches'
    opponent = db.Column(db.String(255))
    venue = db.Column(db.String(255))
    match_number = db.Column(db.Integer, primary_key=True)
    team_score = db.Column(db.String(255))
    opponent_team_score = db.Column(db.String(255))
    overs_played = db.Column(db.Integer)
    result = db.Column(db.String(255))
    player_of_the_match = db.Column(db.String(255), nullable=False)


class Coach(db.Model):
    __tablename__ = 'coach'
    name = db.Column(db.String(255))
    designation = db.Column(db.String(255))
    coach_id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(255))
    experience = db.Column(db.String(512))
    coaching_period = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'user'
    name = db.Column(db.String(128), primary_key=True)
    password_hash = db.Column(db.String(128))


# ---------- ROUTES ----------
@app.route('/')
def index():
    return "Cricket Database deployed successfully!"

# ---------- CLI COMMAND TO CREATE DB ----------
@app.cli.command('init-db')
def init_db():
    """Create tables in remote DB"""
    db.drop_all()
    db.create_all()
    print("✅ Database schema created on remote server.")


if __name__ == '__main__':
    app.run(debug=True)
