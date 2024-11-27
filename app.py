from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session handling

# Database connection (assuming you're using MySQL)
import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="SQL@DBMS",  # Replace with your MySQL password
    database="ICT_2023_CWC"  # Replace with your database name
)

@app.route('/')
def home():
    # Redirect to login if not logged in
    if 'username' not in session:
        return redirect('/login')  # Redirect to login page
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check username and password in the database
        cursor = db_connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Login successful
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect('/')  # Redirect to homepage after login
        else:
            # Login failed
            return render_template('login.html', message="Invalid username or password")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  # Clear session on logout
    return redirect('/login')



# Photo mapping for players and coaches
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
# Player stats with sorting and searching
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

    cursor = db_connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (search_param,))
        players = cursor.fetchall()
        return render_template(
            'players.html', 
            players=players, 
            sort_by=sort_by, 
            order=order, 
            search_query=search_query
        )
    except mysql.connector.Error as e:
        return f"Database Error: {e}"
    finally:
        cursor.close()

# Player name suggestions for autocomplete
@app.route('/player-suggestions', methods=['GET'])
def player_suggestions():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"suggestions": []})

    cursor = db_connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT name FROM player WHERE name LIKE %s LIMIT 10",
            (query + '%',)
        )
        players = cursor.fetchall()
        suggestions = [player['name'] for player in players]
        return jsonify({"suggestions": suggestions})
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Bowler stats with sorting
@app.route('/bowler-stats', methods=['GET'])
def bowler_stats():
    cursor = db_connection.cursor(dictionary=True)
    sort_by = request.args.get('sort_by', 'wickets')
    order = request.args.get('order', 'DESC').upper()

    if sort_by not in ['wickets', 'economy', 'average']:
        sort_by = 'wickets'
    if sort_by in ['economy', 'average']:
        order = 'ASC'
    if order not in ['ASC', 'DESC']:
        order = 'DESC'

    query = f"SELECT * FROM bowler_stats ORDER BY {sort_by} {order}"
    cursor.execute(query)
    bowlers = cursor.fetchall()

    for bowler in bowlers:
        bowler['photo'] = photo_mapping.get(bowler['name'], 'default.jpg')

    return render_template(
        'bowlers.html', 
        bowlers=bowlers, 
        sort_by=sort_by, 
        order=order
    )

# Batsman stats
@app.route('/batsman-stats', methods=['GET'])
def batsman_stats():
    cursor = db_connection.cursor(dictionary=True)
    sort_by = request.args.get('sort_by', 'runs')

    if sort_by not in ['runs', 'average', 'strike_rate']:
        sort_by = 'runs'

    query = f"SELECT * FROM batsmen_stats ORDER BY {sort_by} DESC"
    try:
        cursor.execute(query)
        batsmen = cursor.fetchall()
    except Exception as e:
        print(f"Error querying the view: {e}")
        batsmen = []

    for batsman in batsmen:
        batsman['photo'] = photo_mapping.get(batsman['name'], 'default.jpg')

    return render_template('batsmen.html', batsmen=batsmen)

# Match highlights
@app.route('/match-highlights')
def match_highlights():
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM matches")
    matches = cursor.fetchall()
    return render_template('matches.html', matches=matches)

# Coach details
@app.route('/coach')
def coach():
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM coach")
    coaches = cursor.fetchall()
    for coach in coaches:
        coach['photo'] = photo_mapping.get(coach['name'], 'default.jpg')
    return render_template('coach.html', coaches=coaches)

if __name__ == '__main__':
    app.run(debug=True)
