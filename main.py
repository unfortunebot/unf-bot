import os
import asyncio
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask
from dotenv import load_dotenv
import config
import database

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot aktif"

def keep_alive():
    Thread(target=lambda: app.run(host="0.0.0.0", port=10000), daemon=True).start()

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    reconnect=True
)

def yetki(interaction):
    return any(r.id == config.ALLOWED_ROLE_ID for r in interaction.user.roles)

@bot.event
async def on_ready():
    await database.setup()
    await bot.tree.sync()
    print(f"{bot.user} aktif")

@bot.event
async def on_disconnect():
    print("Discord bağlantısı koptu, tekrar bağlanacak")

@bot.tree.command(name="dm-duyuru")
async def dm_duyuru(interaction: discord.Interaction, rol: discord.Role, mesaj: str):

    if not yetki(interaction):
        return await interaction.response.send_message("Yetkin yok", ephemeral=True)

    await interaction.response.send_message("📨 DM gönderimi başladı")

    basarili = 0
    basarisiz = 0
    uyeler = list(rol.members)

    durum = await interaction.channel.send("📨 DM Durumu %0")

    for i, uye in enumerate(uyeler):
        try:
            await uye.send(f"📢 Duyuru\n\n{mesaj}")
            basarili += 1
        except:
            basarisiz += 1

        yuzde = int(((i+1)/len(uyeler))*100) if uyeler else 100

        await durum.edit(
            content=f"📨 DM Durumu\n\n%{yuzde}\n\nBaşarılı: {basarili}\nBaşarısız: {basarisiz}"
        )

        await asyncio.sleep(0.3)

async def main():
    keep_alive()

    while True:
        try:
            await bot.start(os.getenv("TOKEN"))
        except Exception as e:
            print("Yeniden bağlanıyor:", e)
            await asyncio.sleep(10)

asyncio.run(main())
