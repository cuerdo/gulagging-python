# Telegram Weight Tracker Bot and Web Dashboard

This project combines a Telegram bot and a web dashboard to help users track their weight over time. Users can interact with the bot to log their weight and view their historical data. The web dashboard provides a comprehensive view of all user data and includes a dynamic graph to visualize weight changes over time.

---

## Features

### Telegram Bot
- **Log Weight**: Users can log their weight and the date using the Telegram bot.
- **View History**: Users can retrieve their historical weight data directly in Telegram.
- **Stores Data**: Logs user ID, username, date, and weight in an SQLite database.

### Web Dashboard
- **User Data Table**: Displays all user data in a tabular format.
- **Filter by User**: Filter data by user ID to view specific user entries.
- **Weight Trend Graph**: Visualizes weight changes over time using a line graph embedded in the webpage.

---

## Requirements

### Python Packages
The following Python libraries are required:
- `python-telegram-bot` (for the bot)
- `Flask` (for the web dashboard)
- `sqlite3` (for the database)
- `Matplotlib` (for graph generation)
- `python-dotenv` (to manage the bot token securely)

Install all dependencies using:
```bash
pip install python-telegram-bot Flask matplotlib python-dotenv
```

### Environment Variables
Create a `.env` file in the project directory and add your Telegram bot token:
```
BOT_TOKEN=your-telegram-bot-token
```

---

## Setup Instructions

### 1. Database Initialization
The project uses SQLite for storing user data. The database schema is automatically created when you run the Telegram bot or web app.

### 2. Run the Telegram Bot
Start the Telegram bot using:
```bash
python bot.py
```
- Interact with the bot on Telegram by sending `/start` to log weight.
- Use `/history` to view historical weight entries.

### 3. Run the Web Dashboard
Launch the Flask web app:
```bash
python app.py
```
- Open your browser and go to `http://127.0.0.1:5000/`.
- Filter by user ID to view specific user data.
- The embedded graph visualizes the user's weight changes over time.

---

## Project Structure

```
project/
├── bot.py               # Telegram bot code
├── app.py               # Flask web application code
├── user_data.db         # SQLite database (auto-created)
├── templates/
│   └── index.html       # HTML template for the web dashboard
├── .env                 # Stores the Telegram bot token
└── README.md            # Project documentation
```

---

## Usage

1. Start the bot and log weight by interacting with it on Telegram.
2. Open the web dashboard to view user data and weight trend graphs.

---

## Examples

### Telegram Bot Commands
1. **Log Weight**:
   - `/start`: Begin the logging process.
   - Enter the date (e.g., `2024-12-14`) and weight (e.g., `70`).
2. **View History**:
   - `/history`: Retrieve all historical weight logs.

### Web Dashboard
1. **View All Data**: Navigate to `http://127.0.0.1:5000/`.
2. **Filter by User**: Enter a user ID in the search form and click **Filter**.
3. **View Weight Changes**: The graph below the table displays weight changes over time.

---

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

---

## License

This project is licensed under the APACHE 2.0 License. See the [LICENSE](LICENSE) file for details.