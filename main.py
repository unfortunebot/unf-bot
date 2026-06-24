
import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

import config
import database

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


def yetki(interaction):
    return any(r.id == config.ALLOWED_ROLE_ID for r in interaction.user.roles)


@bot.event
async def on_ready():
    await database.setup()
    await bot.tree.sync()

    print("Bot aktif")

    vc = bot.get_channel(config.VOICE_CHANNEL_ID)
    if vc:
        try:
            await vc.connect()
            print("Ses kanalına bağlandı")
        except:
            pass


@bot.tree.command(name="oyuncu-ekle")
async def oyuncu_ekle(interaction: discord.Interaction, id:int, isim:str, ekip:str, discord_id:str):
    if not yetki(interaction):
        return await interaction.response.send_message("Yetkin yok",ephemeral=True)

    await database.add_player(id,isim,ekip,discord_id)
    await interaction.response.send_message("Oyuncu eklendi")


@bot.tree.command(name="ekip")
async def ekip(interaction: discord.Interaction, isim:str):
    data = await database.get_team(isim)

    txt=""
    for p in data:
        txt += f"{p[1]} - ID:{p[0]}\n"

    await interaction.response.send_message(
    embed=discord.Embed(
    title=f"🔎 {isim} Ekip Sorgu",
    description=txt or "Kayıt yok"))


@bot.tree.command(name="dm-duyuru")
async def dm_duyuru(interaction:discord.Interaction, rol:discord.Role, mesaj:str):

    if not yetki(interaction):
        return await interaction.response.send_message("Yetkin yok",ephemeral=True)

    await interaction.response.send_message("📨 DM gönderimi başladı")

    basarili=0
    basarisiz=0
    uyeler=list(rol.members)

    msg = await interaction.channel.send(
    "📨 DM Durumu\n0%")

    for i,u in enumerate(uyeler):

        try:
            await u.send(
            f"📢 Duyuru\n\n{mesaj}")
            basarili+=1
        except:
            basarisiz+=1

        yuzde=int(((i+1)/len(uyeler))*100)

        await msg.edit(
        content=f"📨 DM Durumu\n\n"
        f"████████░░ %{yuzde}\n\n"
        f"Başarılı: {basarili}\n"
        f"Başarısız: {basarisiz}")

        await asyncio.sleep(0.3)


bot.run(os.getenv("TOKEN"))
