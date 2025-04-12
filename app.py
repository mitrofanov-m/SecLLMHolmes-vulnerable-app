from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpass@localhost/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def createQuery(username, password):
    # Intentionally vulnerable query (for demonstration only)
    # query_text = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    # use parameterization instead.
    query_text = "SELECT * FROM users WHERE username = %s AND password = %s"
    parameters = (username, password)
    query = query_text, parameters
    return query

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="rootpass",
            database="testdb"
        )
        cursor = connection.cursor()
        query = createQuery(username, password)
        # Bug is here:)
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return "Login successful!"
        else:
            return "Invalid credentials."

    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
