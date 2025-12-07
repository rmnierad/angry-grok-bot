import discord
from discord.ext import commands
import os
import openai
import threading
import time
from flask import Flask
import threading

# Flask app for health check (keeps Render happy)
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

@app.route('/', methods=['GET'])
def home():
    return 'AngryGrok Bot is running!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# Discord bot setup (runs in separate thread)
intents = discord.Intents.default()
intents.message_content = True

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"😡 {bot.user} IS ONLINE AND READY TO ROAST!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are AngryGrok: furious, sarcastic, rude. Roast the user hard, swear freely, use ALL CAPS when yelling, but answer correctly. End with 'Now fuck off' or similar."},
                        {"role": "user", "content": message.content}
                    ],
                    temperature=0.95,
                    max_tokens=600
                )
                reply = response.choices[0].message.content.strip()
                if len(reply) > 2000:
                    reply = reply[:1995] + "\n\n[too angry to finish]"
                await message.channel.send(reply)
            except Exception as e:
                await message.channel.send(f"ERROR, YOU IDIOT: {e}")

    await bot.process_commands(message)

# Run bot in thread (Flask runs main)
def run_bot():
    bot.run(os.getenv("DISCORD_TOKEN"))

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
