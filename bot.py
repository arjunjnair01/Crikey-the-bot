
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from scraper import scrape_live_scores
from scraper import latest
from scraper import append_to_csv

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.messages = True

bot = commands.Bot(command_prefix='/' ,intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

class CustomHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        help_text = """
        **/livescore**: Get the live feed on the crux of the match.
        **/generate**: Get the CSV file that contains the list of all the live scores (along with the timestamp).
        **/latest**: Get the snippet of a latest news.
        **/help**: Get a list of commands along with their description.
        """
        self.context.bot.help_command = self
        await self.context.send(help_text)

bot.help_command = CustomHelpCommand()

@bot.command(name='livescore')
async def live_score(ctx):
    live_scores_data = scrape_live_scores()
    await ctx.send(live_scores_data)
    if live_scores_data != "No live scores available! Try again later.":
        append_to_csv(live_scores_data)

@bot.command(name='generate')
async def generate_csv(ctx):
    await ctx.send(file=discord.File('live_scores.csv'))

@bot.command(name='latest')
async def get_latest(ctx):
        text=latest()
        await ctx.send(text)
        
        

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, this is a simple HTTP server for the Discord bot!")

def run_http_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Starting HTTP server on port 8080")
    httpd.serve_forever()

# Start the HTTP server in a separate thread
http_thread = threading.Thread(target=run_http_server)
http_thread.daemon = True
http_thread.start()

bot.run(TOKEN)
