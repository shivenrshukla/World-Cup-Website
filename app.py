from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import MySQLdb.cursors

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key'  # Use a strong secret key in production

# Initialize MySQL and Bcrypt
mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SQL@DBMS'
app.config['MYSQL_DB'] = 'ICT_2023_CWC'

# Route for home page
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))  # Redirect to login page if not logged in

# Route to display player stats
@app.route('/player-stats', methods=['GET'])
def player_stats():
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    search_query = request.args.get('search_query', '').strip()

    valid_sort_fields = ['icc_ranking', 'career_matches', 'name']
    valid_orders = ['asc', 'desc']

    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    if order.lower() not in valid_orders:
        order = 'asc'

    query = f"SELECT * FROM player WHERE name LIKE %s ORDER BY {sort_by} {order.upper()}"
    search_param = f"%{search_query}%"

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute(query, (search_param,))
        players = cur.fetchall()
        return render_template('players.html', players=players, sort_by=sort_by, order=order, search_query=search_query)
    except Exception as e:
        return f"Database Error: {e}"
    finally:
        cur.close()
@app.route('/player/add', methods=['POST'])
def add_player():
    try:
        data = request.form
        jersey_number = data.get('jersey_number')
        name = data.get('name')
        career_matches = data.get('career_matches')
        icc_ranking = data.get('icc_ranking')
        age = data.get('age')

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO player (jersey_number, name, career_matches, icc_ranking, age)
            VALUES (%s, %s, %s, %s, %s)
        """, (jersey_number, name, career_matches, icc_ranking, age))
        mysql.connection.commit()
        cur.close()

        flash("Player added successfully!", "success")
        return redirect(url_for('player_stats'))
    except Exception as e:
        return f"Error adding player: {e}"

# Update Player
@app.route('/player/update/<int:jersey_number>', methods=['POST'])
def update_player(jersey_number):
    try:
        data = request.form
        name = data.get('name')
        career_matches = data.get('career_matches')
        icc_ranking = data.get('icc_ranking')
        age = data.get('age')

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE player 
            SET name = %s, career_matches = %s, icc_ranking = %s, age = %s
            WHERE jersey_number = %s
        """, (name, career_matches, icc_ranking, age, jersey_number))
        mysql.connection.commit()
        cur.close()

        flash("Player updated successfully!", "success")
        return redirect(url_for('player_stats'))
    except Exception as e:
        return f"Error updating player: {e}"

# Delete Player
@app.route('/player/delete/<int:jersey_number>', methods=['POST'])
def delete_player(jersey_number):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM player WHERE jersey_number = %s", (jersey_number,))
        mysql.connection.commit()
        cur.close()

        flash("Player deleted successfully!", "success")
        return redirect(url_for('player_stats'))
    except Exception as e:
        return f"Error deleting player: {e}"
# Photo mapping for players
photo_mapping = {
    'Virat Kohli': 'Virat Kohli.jpg',
    'Rohit Sharma': 'Rohit Sharma.jpg',
    'Shreyas Iyer': 'Shreyas Iyer.jpg',
    'KL Rahul': 'KL Rahul.jpg',
    'Suryakumar Yadav': 'Suryakumar Yadav.jpg',
    'Ravindra Jadeja': 'Ravindra Jadeja.jpg',
    'Ravichandran Ashwin': 'Ravichandran Ashwin.jpg',
    'Ishan Kishan': 'Ishan Kishan.jpg',
    'Shubman Gill': 'Shubman Gill.jpg',
    'Mohammed Shami': 'Mohammad Shami.jpg',
    'Mohammed Siraj': 'Mohammad Siraj.jpg',
    'Shardul Thakur': 'Shardul Thakur.jpg',
    'Kuldeep Yadav': 'Kuldeep Yadav.jpg',
    'Jasprit Bumrah': 'Jasprit Bumrah.jpg',
    'Hardik Pandya': 'Hardik Pandya.jpg',
    'Rahul Dravid': 'Rahul Dravid.jpg',
    'Vikram Rathore': 'Vikram Rathore.jpg',
    'Paras Mhambrey': 'Paras Mhambrey.jpg',
    'T Dilip': 'T Dilip.jpg'
    # Add more player-photo mappings here
}

# Route to display bowler stats
@app.route('/bowler-stats', methods=['GET'])
def bowler_stats():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sort_by = request.args.get('sort_by', 'wickets')  # Default sorting column is 'wickets'
    order = request.args.get('order', 'DESC').upper()  # Default sorting order is 'DESC'

    # Validate input
    if sort_by not in ['wickets', 'economy', 'average']:
        sort_by = 'wickets'
    if sort_by in ['economy', 'average']:
        order = 'ASC'
    if order not in ['ASC', 'DESC']:
        order = 'DESC'

    query = f"SELECT * FROM bowler_stats ORDER BY {sort_by} {order}"
    cur.execute(query)
    bowlers = cur.fetchall()
    for bowler in bowlers:
        bowler['photo'] = photo_mapping.get(bowler['name'], 'default.jpg')

    return render_template('bowlers.html', bowlers=bowlers, sort_by=sort_by, order=order)

# Route to display batsman stats
@app.route('/batsman-stats', methods=['GET'])
def batsman_stats():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sort_by = request.args.get('sort_by', 'runs')  # Default sorting by 'runs'

    if sort_by not in ['runs', 'average', 'strike_rate']:
        sort_by = 'runs'

    query = f"SELECT * FROM batsmen_stats ORDER BY {sort_by} DESC"
    try:
        cur.execute(query)
        batsmen = cur.fetchall()
    except Exception as e:
        print(f"Error querying the view: {e}")
        batsmen = []  # Fallback in case of an error

    for batsman in batsmen:
        batsman['photo'] = photo_mapping.get(batsman['name'], 'default.jpg')

    return render_template('batsmen.html', batsmen=batsmen)

# Route for player suggestions (auto-complete)
@app.route('/player-suggestions', methods=['GET'])
def player_suggestions():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"suggestions": []})

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("SELECT name FROM player WHERE name LIKE %s LIMIT 10", (query + '%',))
        players = cur.fetchall()

        suggestions = [player['name'] for player in players]

        return jsonify({"suggestions": suggestions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

# Route for match highlights
@app.route('/match-highlights')
def match_highlights():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM matches")
    matches = cur.fetchall()
    return render_template('matches.html', matches=matches)



# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Query the database for user
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user['password_hash'], password):  # Compare hashed password
            flash("Login Successful!", "success")
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

# Register Route (For Admin or Testing)
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
    mysql.connection.commit()
    cur.close()

    flash("User registered successfully!", "success")
    return redirect(url_for("login"))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if username already exists
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            flash("Username already exists! Please choose a different one.", "danger")
            return redirect(url_for('signup'))

        # Insert the new user into the database
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash("User registered successfully! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/coach', methods=['GET'])
def coach():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("SELECT * FROM coach")
        coaches = cur.fetchall()
        return render_template('coach.html', coaches=coaches)
    except Exception as e:
        return f"Database Error: {e}"
    finally:
        cur.close()


@app.route('/coach/add', methods=['POST'])
def add_coach():
    # Get data from the form
    coach_id = request.form['coach_id']  # Assuming you're adding coach_id manually for now
    name = request.form['name']
    designation = request.form['designation']
    experience = request.form['experience']
    nationality = request.form['nationality']
    coaching_period = request.form['coaching_period']

    # Validate the coaching period is a number
    if not coaching_period.isdigit():
        flash('Coaching period must be a number.', 'danger')
        return redirect(request.url)

    # Insert into the database (including coach_id if needed)
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        query = """
            INSERT INTO coach (coach_id, name, designation, nationality, experience, coaching_period)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (coach_id, name, designation, nationality, experience, int(coaching_period)))
        mysql.connection.commit()
        flash('Coach added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding coach: {e}', 'danger')
    finally:
        cur.close()

    return redirect(url_for('coach'))  # Redirect back to the coaches page



@app.route('/coach/delete/<int:coach_id>', methods=['POST'])
def delete_coach(coach_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM coach WHERE coach_id = %s", (coach_id,))
        mysql.connection.commit()
        flash("Coach deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting coach: {e}", "danger")
    finally:
        cur.close()
    return redirect(url_for('coach'))

if __name__ == '__main__':
    app.run(debug=True)