from flask import Flask, render_template,request, jsonify
import mysql.connector

app = Flask(__name__)

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shiven29@sql",  # Your MySQL password
    database="ict_2023_cwc"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/player-stats', methods=['GET'])
def player_stats():
    # Get query parameters for sorting and searching
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    search_query = request.args.get('search_query', '').strip()  # Get the search query from the request

    # Validate inputs
    valid_sort_fields = ['icc_ranking', 'career_matches', 'name']
    valid_orders = ['asc', 'desc']

    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    if order.lower() not in valid_orders:
        order = 'asc'

    # Construct the query
    query = f"SELECT * FROM player WHERE name LIKE %s ORDER BY {sort_by} {order.upper()}"
    search_param = f"%{search_query}%"  # Use wildcard for partial match

    # Execute the query
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

@app.route('/player-suggestions', methods=['GET'])
def player_suggestions():
    query = request.args.get('q', '').strip()  # Get the search query from the request
    if not query:
        return jsonify({"suggestions": []})  # Return an empty list if the query is empty

    cursor = db_connection.cursor(dictionary=True)

    try:
        # Search for player names that start with the query (case insensitive)
        cursor.execute(
            "SELECT name FROM player WHERE name LIKE %s LIMIT 10",
            (query + '%',)
        )
        players = cursor.fetchall()

        # Extract names from the database results
        suggestions = [player['name'] for player in players]

        return jsonify({"suggestions": suggestions})
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# @app.route('/player-stats')
# def player_stats():
#     sort_by = request.args.get('sort_by', 'name')
#     order = request.args.get('order', 'asc')
    

#     valid_sort_fields = ['icc_ranking', 'career_matches', 'name']
#     valid_orders = ['asc', 'desc']
   
#     cursor = db_connection.cursor(dictionary=True)

#     query = f"SELECT * FROM player ORDER BY {sort_by} {order.upper()}"

#     try:
#         cursor.execute(query)
#         players = cursor.fetchall()

#         if not players:
#             players = []
        
#         return render_template('players.html', players=players, sort_by=sort_by, order=order)
#     except mysql.connector.Error as e:
#         return f"Error: {e}"

#     finally:
#         cursor.close()

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
  

@app.route('/bowler-stats', methods=['GET'])
def bowler_stats():
    cursor = db_connection.cursor(dictionary=True)
    sort_by = request.args.get('sort_by', 'wickets')  # Default sorting column is 'wickets'
    order = request.args.get('order', 'DESC').upper()  # Default sorting order is 'DESC'

    # Validate the input
    if sort_by not in ['wickets', 'economy', 'average']:
        sort_by = 'wickets'
    if order not in ['ASC', 'DESC']:
        order = 'DESC'

    # Query the database
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

@app.route('/batsman-stats', methods=['GET'])
def batsman_stats():
    cursor = db_connection.cursor(dictionary=True)
    sort_by = request.args.get('sort_by', 'runs')  # Default sorting by 'runs'

    # Validate sort_by parameter
    if sort_by not in ['runs', 'average', 'strike_rate']:
        sort_by = 'runs'

    # Query the view instead of the table
    query = f"SELECT * FROM batsmen_stats ORDER BY {sort_by} DESC"
    try:
        cursor.execute(query)
        batsmen = cursor.fetchall()
    except Exception as e:
        print(f"Error querying the view: {e}")
        batsmen = []  # Fallback in case of an error
    for batsman in batsmen:
        batsman['photo'] = photo_mapping.get(batsman['name'], 'default.jpg') 

    return render_template('batsmen.html', batsmen=batsmen)


@app.route('/match-highlights')
def match_highlights():
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM matches")
    matches = cursor.fetchall()
    return render_template('matches.html', matches=matches)

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
