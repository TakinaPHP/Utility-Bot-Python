import discord
from discord.ext import commands
import youtube_dl

# Set up the bot with a command prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Set up youtube_dl options
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,  # download only audio
    'audioformat': 'mp3',  # save as mp3
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',  # save file as <extractor>-<id>-<title>
    'restrictfilenames': True,
    'noplaylist': True,  # download only single song, not playlist
}

ffmpeg_options = {
    'options': '-vn'  # no video
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command()
async def join(ctx):
    """Joins the voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def leave(ctx):
    """Leaves the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command()
async def play(ctx, *, url):
    """Plays a song from a URL."""
    if not ctx.voice_client:
        await ctx.send("I'm not connected to a voice channel. Use !join first.")
        return

    async with ctx.typing():
        info = ytdl.extract_info(url, download=False)
        url = info['formats'][0]['url']
        ctx.voice_client.stop()
        ctx.voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options))
    
    await ctx.send(f'Now playing: {info["title"]}')

@bot.command()
async def pause(ctx):
    """Pauses the currently playing song."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Paused the music.")
    else:
        await ctx.send("No music is playing.")

@bot.command()
async def resume(ctx):
    """Resumes the currently paused song."""
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resumed the music.")
    else:
        await ctx.send("No music is paused.")

@bot.command()
async def stop(ctx):
    """Stops the currently playing song."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Stopped the music.")
    else:
        await ctx.send("No music is playing.")

# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot.run('YOUR_BOT_TOKEN')
