import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

#on_ready
@bot.event
async def on_ready():
    try:
        bot.remove_command("help") #helpは敵。
    except Exception as error:
        print(f"[Error] {error}")
    
    try:
        bot.load_extension("cogs.command")
    except Exception as error:
        print(f"[Error] cogs.command → {error}")
    else:
        print("[System] cogs.command load")
        
    print("[System] on_ready!")

#on_connect
@bot.event
async def on_connect():
    print("[System] on_connect!")
    
#command log
@bot.event
async def on_command(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        print(f"[Log] {ctx.author} ({ctx.author.id}) → {ctx.command} @DM")
    else:
        print(f"[Log] {ctx.author} ({ctx.author.id}) → {ctx.command} #{ctx.channel} ({ctx.channel.id}) in {ctx.guild} ({ctx.guild.id})")

print("[System] booting....")
bot.run("YoUr BoT tOkEn HeRe")
