from flask import Flask, render_template, request
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
import datetime

# Initialize the Flask app
app = Flask(__name__)

# Function to retrieve data from the database
def get_all_data(user_id=None):
    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()
    
    # Query to retrieve all data or filter by user_id
    if user_id:
        cursor.execute("SELECT user_id, username, date, weight FROM user_info WHERE user_id = ?", (user_id,))
    else:
        cursor.execute("SELECT user_id, username, date, weight FROM user_info")
    
    rows = cursor.fetchall()
    connection.close()
    return rows

# Function to retrieve weight data for graphing
def get_weight_data(user_id):
    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT date, weight FROM user_info WHERE user_id = ? ORDER BY date", (user_id,))
    rows = cursor.fetchall()
    connection.close()
    return rows

# Function to generate a graph as a base64-encoded image
def generate_graph(user_id):
    # Retrieve weight data for the user
    data = get_weight_data(user_id)
    if not data:
        return None

    # Extract dates and weights
    dates = [datetime.datetime.strptime(row[0], "%Y-%m-%d").date() for row in data]
    weights = [float(row[1]) for row in data]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, weights, marker="o")
    plt.title(f"Weight Changes Over Time for User {user_id}")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.grid(True)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()

    # Encode the image as a base64 string
    graph_url = base64.b64encode(img.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{graph_url}"

# Home route to display the data with an optional user filter
@app.route("/", methods=["GET", "POST"])
def index():
    user_id = None
    graph_url = None
    if request.method == "POST":
        user_id = request.form.get("user_id")
        if user_id:
            graph_url = generate_graph(user_id)

    data = get_all_data(user_id=user_id)
    return render_template("index.html", data=data, user_id=user_id, graph_url=graph_url)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
