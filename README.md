# Telegram File Manager Bot

A Telegram bot for managing files in the cloud. Users can upload files manually through the bot, then perform various actions like searching, listing, and deleting files.

## Features

- **File Upload**: Upload documents directly to the bot.
- **File Search**: Search for files by name or caption using keywords.
- **File Listing**: View all stored files.
- **File Deletion**: Delete specific files by name.
- **Database Storage**: Files metadata stored in SQLite database.
- **Secure Token Handling**: Bot token loaded from environment variables.

## Prerequisites

- Python 3.7+
- A Telegram Bot Token (obtained from [@BotFather](https://t.me/botfather))

## Installation

1. Clone or download this repository.
2. Navigate to the project directory.
3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Setup

1. Create a `.env` file in the root directory.
2. Add your Telegram Bot Token to the `.env` file:

   ```
   BOT_TOKEN=your_bot_token_here
   ```

3. Run the bot:

   ```
   python bot.py
   ```

## Usage

Start a chat with your bot on Telegram. The bot will guide you through the available commands.

### Available Commands

- `/start` or `/help`: Display the welcome message and list of commands.
- `/upload`: Upload a file (send a document to the bot).
- `/search <keyword>`: Search for files containing the keyword in name or caption.
- `/list`: Show all stored files.
- `/delete <filename>`: Delete a file by its exact filename.

### How It Works

1. **Upload Files**: Users must upload files manually by sending documents to the bot. The bot will store the file in the `files/` directory and record metadata in the database.
2. **Manage Files**: Once uploaded, use the commands to search, list, or delete files.

## Database Schema

The bot uses a SQLite database (`files.db`) with the following table:

### `files` Table

| Column      | Type    | Description                  |
|-------------|---------|------------------------------|
| id          | INTEGER | Primary key, auto-increment  |
| file_name   | TEXT    | Name of the uploaded file    |
| file_id     | TEXT    | Telegram file ID             |
| caption     | TEXT    | Optional caption for the file|
| upload_date | TEXT    | Date and time of upload      |

## Project Structure

- `bot.py`: Main bot script
- `database.py`: Database operations
- `requirements.txt`: Python dependencies
- `files/`: Directory for storing uploaded files
- `files.db`: SQLite database file
- `.env`: Environment variables (not included in repo)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
