import discord
from discord.ext import commands

# Set up the bot with a command prefix
intents = discord.Intents.default()
intents.members = True  # Enable the members intent to kick/ban users
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kicks a member from the server."""
    if member == ctx.author:
        await ctx.send("You cannot kick yourself.")
        return

    embed = discord.Embed(title="User  Kicked", color=discord.Color.red())
    embed.add_field(name="User ", value=f"{member.mention} ({member.id})", inline=True)
    embed.add_field(name="Kicked by", value=f"{ctx.author.mention}", inline=True)
    embed.add_field(name="Reason", value=reason or "No reason provided", inline=True)

    await member.kick(reason=reason)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bans a member from the server."""
    if member == ctx.author:
        await ctx.send("You cannot ban yourself.")
        return

    embed = discord.Embed(title="User  Banned", color=discord.Color.red())
    embed.add_field(name="User ", value=f"{member.mention} ({member.id})", inline=True)
    embed.add_field(name="Banned by", value=f"{ctx.author.mention}", inline=True)
    embed.add_field(name="Reason", value=reason or "No reason provided", inline=True)

    await member.ban(reason=reason)
    await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to kick members.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Member not found. Please mention a valid member.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to ban members.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Member not found. Please mention a valid member.")

# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot.run('YOUR_BOT_TOKEN')
