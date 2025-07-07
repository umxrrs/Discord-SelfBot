# QuranBot

**QuranBot** is a *Discord bot* designed to fetch verses from the Quran in both **Arabic** and **English** (Sahih International translation) using the [Al Quran Cloud API](http://api.alquran.cloud/). It supports **slash commands** for modern Discord interactions, traditional prefix-based commands, and individual slash commands for every Surah, making it easy to access specific verses.

## Features

- **Slash Commands**: Use `/quran` with a Surah:Ayah reference (e.g., `/quran 2:45`) to retrieve a verse.
- **Surah-Specific Commands**: Each of the 114 Surahs has its own slash command (e.g., `/al-fatiha`, `/al-baqara`) for quick verse access.
- **Traditional Command**: Use `!quran` with a Surah:Ayah format (e.g., `!quran 2:45`) for legacy command support.
- **Rich Embeds**: Verses are displayed in clean Discord embeds with Arabic text, English translation, and Surah details.
- **Error Handling**: Gracefully handles invalid inputs, API errors, or unavailable verses with user-friendly messages.

## Requirements

- **Python 3.8+**
- **Dependencies** (install via `pip`):
  ```bash
  pip install discord.py requests
  ```

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/umxrrs/QuranBot
   cd QuranBot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Bot**:
   - Put your Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications). in `config.json`  
   - Ensure your bot has the necessary permissions (`Send Messages`, `Embed Links`) and intents enabled (`message_content`).

4. **Run the Bot**:
   ```bash
   python quran.py
   ```

## Usage

- **Slash Command Example**:
  - Use `/quran 2:45` to fetch Surah Al-Baqara, Ayah 45.
  - Use `/al-fatiha 1` to fetch Ayah 1 from Surah Al-Fatiha.

- **Traditional Command Example**:
  - Use `!quran 2:45` in a text channel to fetch the same verse.

- **Output**:
  The bot responds with an embed containing:
  - The Surah name and verse reference (e.g., "Al-Baqara 2:45 - Sahih International").
  - The Arabic text of the verse.
  - The English translation.
  - A footer crediting the bot creator.

## Example Output

For `/quran 2:45`:
> **Al-Baqara 2:45 - Sahih International**
> **Arabic**: وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ ۚ وَإِنَّهَا لَكَبِيرَةٌ إِلَّا عَلَى الْخَاشِعِينَ
> **English**: And seek help through patience and prayer. Indeed, it is difficult except for the humbly submissive [to Allah].
> *QuranBot By Umar*

## Notes

- The bot uses the [Al Quran Cloud API](http://api.alquran.cloud/) for verse data. Ensure a stable internet connection.
- Slash commands are synced globally on bot startup, which may take a few minutes to propagate.
- Invalid Surah or Ayah inputs (e.g., Surah > 114 or Ayah <= 0) will return an error message.

## Contributing

Feel free to submit **pull requests** or open **issues** for bug reports, feature requests, or improvements. Ensure your code follows the existing style and includes clear comments.

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

- Built by **Umar**.
- Powered by the [Al Quran Cloud API](http://api.alquran.cloud/).
- Uses [discord.py](https://github.com/Rapptz/discord.py) for Discord integration.

---

Let me know if you want to tweak anything or add more sections!
