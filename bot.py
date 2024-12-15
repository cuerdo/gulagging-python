import sqlite3
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Define conversation states
ASK_DATE, ASK_WEIGHT = range(2)

# Database setup
def setup_database():
    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            date TEXT,
            weight TEXT
        )
    """)
    connection.commit()
    connection.close()

# Store data in the database
def store_data(user_id, username, date, weight):
    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO user_info (user_id, username, date, weight) VALUES (?, ?, ?, ?)",
        (user_id, username, date, weight)
    )
    connection.commit()
    connection.close()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Hello! I need some information. Please enter the date (in YYYY-MM-DD format):"
    )
    return ASK_DATE

# Handle date input
async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    date = update.message.text
    context.user_data['date'] = date  # Store the date in user data
    await update.message.reply_text("Thank you! Now, please enter your weight (in kilograms):")
    return ASK_WEIGHT

# Handle weight input
async def ask_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    weight = update.message.text
    context.user_data['weight'] = weight  # Store the weight in user data

    # Store data in the database
    user_id = update.message.from_user.id  # Telegram User ID
    username = update.message.from_user.username or "Unknown"  # Telegram Username (if available)
    date = context.user_data['date']
    store_data(user_id, username, date, weight)

    # Respond with the collected information
    await update.message.reply_text(
        f"Got it! You entered:\nDate: {date}\nWeight: {weight} kg\n\nYour data has been saved!",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Retrieve historical data command
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    data = retrieve_data(user_id)

    if data:
        history_message = "Here is your historical data:\n"
        for date, weight in data:
            history_message += f"- Date: {date}, Weight: {weight} kg\n"
        await update.message.reply_text(history_message)
    else:
        await update.message.reply_text("No historical data found.")

# Retrieve user data from the database
def retrieve_data(user_id):
    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT date, weight FROM user_info WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    connection.close()
    return rows

# Cancel the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation canceled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Main function
def main():
    # Setup the database
    setup_database()

    # Create the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Create a conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_date)],
            ASK_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_weight)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add conversation and history handlers to the application
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("history", history))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
