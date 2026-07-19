import discord
from discord.ext import commands
from discord import app_commands
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# Веб-сервер для Render
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

Thread(target=run_web, daemon=True).start()

# Настройки Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Бот {bot.user} запущен!")

    try:
        synced = await bot.tree.sync()
        print(f"Синхронизировано команд: {len(synced)}")
    except Exception as e:
        print(f"Ошибка синхронизации: {e}")

# Команда /ping
@bot.tree.command(name="ping", description="Проверка работы бота")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

# Проверка токена
token = os.getenv("TOKEN")
print("TOKEN найден:", token is not None)

if not token:
    print("ОШИБКА: переменная TOKEN не найдена!")
else:
    bot.run(token)
