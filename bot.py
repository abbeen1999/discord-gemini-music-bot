import discord
from discord.ext import commands
import openai
import yt_dlp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# AI Chat Command
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

@bot.command(name='tanya')
async def tanya_gemini(ctx, *, pertanyaan):
    await ctx.send("🧠 Sedang berpikir dengan Gemini...")
    try:
        response = model.generate_content(pertanyaan)
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f"❌ Terjadi error: {e}")



# Join voice channel
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("✅ Sudah masuk voice channel.")
    else:
        await ctx.send("❌ Kamu harus ada di voice channel dulu.")

# Play music from YouTube
@bot.command()
async def play(ctx, *, url):
    if not ctx.voice_client:
        await ctx.invoke(join)

    FFMPEG_OPTIONS = {'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio'}

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        ctx.voice_client.stop()
        ctx.voice_client.play(source)
        await ctx.send(f"🎵 Memutar: {info['title']}")

# Stop music
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🛑 Musik dihentikan dan bot keluar.")

bot.run(TOKEN)
