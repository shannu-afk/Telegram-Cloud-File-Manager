from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from datetime import datetime
from database import init_db, add_file, search_file, delete_file
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Securely loaded from .env
FILES_DIR = "files"

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

init_db()

# --- COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📁 Welcome to *Your Cloud File Manager Bot*!\n\n"
        "You can:\n"
        "/upload — Upload a file\n"
        "/search <keyword> — Search files\n"
        "/delete <filename> — Delete file\n"
        "/list — Show all files\n"
        "/help — Show this menu",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# --- FILE UPLOAD ---
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc:
        await update.message.reply_text("Please send a valid document.")
        return

    file_name = doc.file_name
    file_id = doc.file_id
    caption = update.message.caption or "No caption"
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    add_file(file_name, file_id, caption, upload_date)
    file = await context.bot.get_file(file_id)
    await file.download_to_drive(os.path.join(FILES_DIR, file_name))

    await update.message.reply_text(f"✅ File '{file_name}' uploaded successfully!")

# --- SEARCH FILE ---
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /search <keyword>")
        return

    keyword = " ".join(context.args)
    results = search_file(keyword)

    if not results:
        await update.message.reply_text("❌ No matching files found.")
        return

    for name, fid in results:
        await update.message.reply_document(document=fid, caption=f"📄 {name}")

# --- LIST FILES ---
async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = os.listdir(FILES_DIR)
    if not files:
        await update.message.reply_text("📂 No files available.")
    else:
        msg = "📁 *Stored Files:*\n" + "\n".join(f"• {f}" for f in files)
        await update.message.reply_text(msg, parse_mode="Markdown")

# --- DELETE FILE ---
async def delete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /delete <filename>")
        return

    filename = " ".join(context.args)
    path = os.path.join(FILES_DIR, filename)

    if os.path.exists(path):
        os.remove(path)
        delete_file(filename)
        await update.message.reply_text(f"🗑️ File '{filename}' deleted successfully!")
    else:
        await update.message.reply_text("❌ File not found.")

# --- MAIN APP ---
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("list", list_files))
app.add_handler(CommandHandler("delete", delete_cmd))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

print("🤖 Bot is running...")
app.run_polling()
