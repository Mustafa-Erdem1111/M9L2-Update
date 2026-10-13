import discord
from discord.ext import commands
import requests
import os
import traceback
from gtts import gTTS
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.command()
async def start(ctx):
    await ctx.send(
        "Merhaba! Ben hava durumunu yazılı ve sesli "
        "olarak bildiren bir botum! 🌦️\n\n"
        "Kullanım:\n"
        "!weather Mardin\n"
        "!weather İstanbul\n"
        "!weather Batman\n\n"
        "Şehir yazmazsan Mardin'in hava durumunu gösteririm."
    )


@bot.command()
async def weather(ctx, *, city="Mardin"):
    filename = "hava_durumu.mp3"

    try:
        # Şehir adındaki boşlukları URL için düzenle
        city_url = requests.utils.quote(city.strip())

        # Hava durumunu al
        url = "https://wttr.in/" + city_url + "?format=3"
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        weather_text = response.text.strip()

        if not weather_text or "Unknown location" in weather_text:
            await ctx.send(
                "Bu şehri bulamadım dostum. "
                "Şehir adını kontrol edip tekrar dene."
            )
            return

        # Yazılı hava durumu
        await ctx.send("🌦️ " + weather_text)

        # Türkçe ses oluştur
        print("gTTS değeri:", gTTS)
        print("gTTS türü:", type(gTTS))

        tts = gTTS(
            text=weather_text,
            lang="tr"
        )

        tts.save(filename)

        # Ses dosyasını gönder
        if os.path.isfile(filename):
            await ctx.send(
                "🔊 " + city + " için sesli hava durumu:",
                file=discord.File(filename)
            )

    except Exception as e:
        print("HATA TÜRÜ:", type(e).__name__)
        print("HATA DETAYI:", str(e))
        traceback.print_exc()

        await ctx.send(
            "Hava durumu veya ses oluşturulurken hata oluştu dostum. "
            "Terminal mesajını kontrol edelim."
        )

    finally:
        if os.path.isfile(filename):
            try:
                os.remove(filename)
            except OSError:
                pass


@bot.event
async def on_ready():
    print("Bot hazır!")
    print("Bot adı:", bot.user)


bot.run(TOKEN)
