from flask import Flask, render_template, request
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
import datetime

# Initialize the Flask app
app = Flask(__name__)

# Function to retrieve all data or filter by user_id
def get_all_data(user_id=None):
    connection = sqlite3.connect("db/user_data.db")
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
    connection = sqlite3.connect("db/user_data.db")
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
        print(f"No data found for user_id: {user_id}")
        return None

    # Extract dates and weights
    dates = [datetime.datetime.strptime(row[0], "%Y-%m-%d").date() for row in data]
    weights = [float(row[1]) for row in data]

    # Debugging: Print the extracted data
    print(f"Generating graph for user_id: {user_id}, Dates: {dates}, Weights: {weights}")

    # Create the plot with a modern style
    plt.figure(figsize=(12, 6))
    plt.style.use("seaborn-v0_8-whitegrid")  # Use a vibrant style

    # Plot the data
    plt.plot(dates, weights, marker="o", linestyle="-", color="#4CAF50", markersize=8, linewidth=2, label="Weight (kg)")

    # Add title and labels
    plt.title(f"Weight Changes Over Time for User {user_id}", fontsize=16, fontweight="bold", color="#333")
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Weight (kg)", fontsize=12)

    # Add grid and legend
    plt.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)
    plt.legend(fontsize=12, loc="upper left")

    # Rotate date labels for better visibility
    plt.xticks(rotation=45)

    # Adjust layout for aesthetics
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format="png", dpi=100, bbox_inches="tight")
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
        print(f"User ID received: {user_id}")  # Debugging
        if user_id:
            graph_url = generate_graph(user_id)
            print(f"Graph URL generated: {bool(graph_url)}")  # Debugging

    data = get_all_data(user_id=user_id)
    print(f"Data retrieved for user_id={user_id}: {data}")  # Debugging
    return render_template("index.html", data=data, user_id=user_id, graph_url=graph_url)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)