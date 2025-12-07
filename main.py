import discord
from discord.ext import commands
import os
import openai
import threading
import time
import requests

intents = discord.Intents.default()
intents.message_content = True

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ANGRYGROK {bot.user} IS ONLINE AND READY TO FUCK SHIT UP")
    
    # Keep-alive pinger — YOUR EXACT URL
    def keep_awake():
        url = "https://angry-grok-bot-ryan1715.repl.app"
        while True:
            try:
                requests.get(url, timeout=10)
            except:
                pass
            time.sleep(300)

    threading.Thread(target=keep_awake, daemon=True).start()

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
                        {"role": "system", "content": "You are AngryGrok: permanently furious, sarcastic, rude. Roast the user hard, swear freely, use ALL CAPS when yelling, but answer correctly. End with 'Now fuck off' or similar."},
                        {"role": "user", "content": message.content}
                    ],
                    temperature=0.95,
                    max_tokens=600
                )
                reply = response.choices[0].message.content
                if len(reply) > 2000:
                    reply = reply[:1995] + "\n\n[too angry to finish]"
                await message.channel.send(reply)
            except Exception as e:
                await message.channel.send(f"ERROR, YOU IDIOT: {e}")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
