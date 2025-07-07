import discord
from discord.ext import commands
import requests
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

class QuranBot(commands.Bot):
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        await super().on_command_error(ctx, error)

    async def setup_hook(self):
       
        await self.tree.sync()
        print("Slash commands synced globally!")

bot = QuranBot(command_prefix="", help_command=None, intents=intents)

TOKEN = 'BOT_TOKEN_HERE'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


SURAH_MAP = {
    "al-fatiha": 1, "al-baqara": 2, "al-imran": 3, "an-nisa": 4, "al-maida": 5,
    "al-anam": 6, "al-araf": 7, "al-anfal": 8, "at-tawba": 9, "yunus": 10,
    "hud": 11, "yusuf": 12, "ar-rad": 13, "ibrahim": 14, "al-hijr": 15,
    "an-nahl": 16, "al-isra": 17, "al-kahf": 18, "maryam": 19, "ta-ha": 20,
    "al-anbiya": 21, "al-hajj": 22, "al-muminun": 23, "an-nur": 24, "al-furqan": 25,
    "ash-shuara": 26, "an-naml": 27, "al-qasas": 28, "al-ankabut": 29, "ar-rum": 30,
    "luqman": 31, "as-sajda": 32, "al-ahzab": 33, "saba": 34, "fatir": 35,
    "ya-sin": 36, "as-saffat": 37, "sad": 38, "az-zumar": 39, "ghafir": 40,
    "fussilat": 41, "ash-shura": 42, "az-zukhruf": 43, "ad-dukhan": 44, "al-jathiya": 45,
    "al-ahqaf": 46, "muhammad": 47, "al-fath": 48, "al-hujurat": 49, "qaf": 50,
    "adh-dhariyat": 51, "at-tur": 52, "an-najm": 53, "al-qamar": 54, "ar-rahman": 55,
    "al-waqia": 56, "al-hadid": 57, "al-mujadila": 58, "al-hashr": 59, "al-mumtahina": 60,
    "as-saff": 61, "al-jumua": 62, "al-munafiqun": 63, "at-taghabun": 64, "at-talaq": 65,
    "at-tahrim": 66, "al-mulk": 67, "al-qalam": 68, "al-haqqa": 69, "al-maarij": 70,
    "nuh": 71, "al-jinn": 72, "al-muzzammil": 73, "al-muddathir": 74, "al-qiyama": 75,
    "al-insan": 76, "al-mursalat": 77, "an-naba": 78, "an-naziat": 79, "abasa": 80,
    "at-takwir": 81, "al-infitar": 82, "al-mutaffifin": 83, "al-inshiqaq": 84, "al-buruj": 85,
    "at-tariq": 86, "al-ala": 87, "al-ghashiya": 88, "al-fajr": 89, "al-balad": 90,
    "ash-shams": 91, "al-lail": 92, "ad-duha": 93, "ash-sharh": 94, "at-tin": 95,
    "al-alaq": 96, "al-qadr": 97, "al-bayyina": 98, "az-zalzala": 99, "al-adiyat": 100,
    "al-qaria": 101, "at-takathur": 102, "al-asr": 103, "al-humaza": 104, "al-fil": 105,
    "quraysh": 106, "al-maun": 107, "al-kawthar": 108, "al-kafirun": 109, "an-nasr": 110,
    "al-masad": 111, "al-ikhlas": 112, "al-falaq": 113, "an-nas": 114
}


@bot.command(name="quran", aliases=["Quran"])
async def quran(ctx, *, input_text=""):
    try:
        if not input_text:
            return

        reference = input_text.split(':')
        if len(reference) != 2:
            return

        surah, ayah = map(int, reference)

        if surah <= 0 or surah > 114 or ayah <= 0:
            await ctx.send("Could not find the verse. Please check the Surah and Ayah.")
            return

        response = requests.get(f'http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.sahih')
        data = response.json()

        if data['code'] != 200:
            await ctx.send("Could not find the verse. Please check the Surah and Ayah.")
            return

        verse_text_en = data['data']['text']
        surah_name = data['data']['surah']['englishName']
        ayah_number = data['data']['numberInSurah']

        arabic_response = requests.get(f'http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/ar.alafasy')
        arabic_data = arabic_response.json()
        verse_text_ar = arabic_data['data']['text'] if arabic_data['code'] == 200 else "Arabic text unavailable"

        embed = discord.Embed(title=f"{surah_name} {surah}:{ayah_number} - Sahih International", color=0x00FF00)
        embed.add_field(name="Arabic", value=verse_text_ar, inline=False)
        embed.add_field(name="English", value=verse_text_en, inline=False)
        embed.set_footer(text="QuranBot By Umar <3")

        await ctx.send(embed=embed)

    except Exception:
        await ctx.send("Could not find the verse. Please check the Surah and Ayah.")

@app_commands.command(name="quran", description="Get a Quran verse by Surah and Ayah (e.g., 2:45)")
@app_commands.describe(reference="The Surah and Ayah in the format Surah:Ayah (e.g., 2:45)")
async def quran_slash(interaction: discord.Interaction, reference: str):
    try:
        reference_parts = reference.split(':')
        if len(reference_parts) != 2:
            await interaction.response.send_message("Please use the format Surah:Ayah (e.g., 2:45).")
            return

        surah, ayah = map(int, reference_parts)

        if surah <= 0 or surah > 114 or ayah <= 0:
            await interaction.response.send_message("Could not find the verse. Please check the Surah and Ayah.")
            return

        response = requests.get(f'http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.sahih')
        data = response.json()

        if data['code'] != 200:
            await interaction.response.send_message("Could not find the verse. Please check the Surah and Ayah.")
            return

        verse_text_en = data['data']['text']
        surah_name = data['data']['surah']['englishName']
        ayah_number = data['data']['numberInSurah']

        arabic_response = requests.get(f'http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/ar.alafasy')
        arabic_data = arabic_response.json()
        verse_text_ar = arabic_data['data']['text'] if arabic_data['code'] == 200 else "Arabic text unavailable"

        embed = discord.Embed(title=f"{surah_name} {surah}:{ayah_number} - Sahih International", color=0x00FF00)
        embed.add_field(name="Arabic", value=verse_text_ar, inline=False)
        embed.add_field(name="English", value=verse_text_en, inline=False)
        embed.set_footer(text="QuranBot By Umar <3")

        await interaction.response.send_message(embed=embed)

    except Exception:
        await interaction.response.send_message("Could not find the verse. Please check the Surah and Ayah.")


for surah_name, surah_number in SURAH_MAP.items():
    @app_commands.command(name=surah_name, description=f"Get a verse from {surah_name.replace('-', ' ').title()} (e.g., 2:45)")
    @app_commands.describe(reference="The Ayah in the format Ayah (e.g., 2:45)")
    async def surah_slash(interaction: discord.Interaction, reference: str, surah_number=surah_number):
        try:
            reference_parts = reference.split(':')
            if len(reference_parts) != 2:
                await interaction.response.send_message("Please use the format Surah:Ayah (e.g., 2:45).")
                return

            surah = surah_number
            ayah = int(reference_parts[1])

            if surah <= 0 or surah > 114 or ayah <= 0:
                await interaction.response.send_message("Could not find the verse. Please check the Surah and Ayah.")
                return

            response = requests.get(f'http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.sahih')
            data = response.json()

            if data['code'] != 200:
                await interaction.response.send_message("Could not find the verse. Please check the Surah and Ayah.")
                return

            verse_text_en = data['data']['text']
            surah_name = data['data']['surah']['englishName']
            ayah_number = data['data']['numberInSurah']

            arabic_response = requests.get(f'http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/ar.alafasy')
            arabic_data = arabic_response.json()
            verse_text_ar = arabic_data['data']['text'] if arabic_data['code'] == 200 else "Arabic text unavailable"

            embed = discord.Embed(title=f"{surah_name} {surah}:{ayah_number} - Sahih International", color=0x00FF00)
            embed.add_field(name="Arabic", value=verse_text_ar, inline=False)
            embed.add_field(name="English", value=verse_text_en, inline=False)
            embed.set_footer(text="QuranBot By Umar <3")

            await interaction.response.send_message(embed=embed)

        except Exception:
            await interaction.response.send_message("Could not find the verse. Please check the Surah and Ayah.")

    
    bot.tree.add_command(surah_slash)


bot.tree.add_command(quran_slash)

bot.run(TOKEN)
