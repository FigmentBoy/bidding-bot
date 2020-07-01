from dotenv import load_dotenv
import os
from discord.utils import get
from discord.ext import commands
import discord

modules = [
    "Cogs.footballAPI"
]

def display_time(seconds, granularity=2):
    result = []
    intervals =  (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
        )
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name[:-1]
            result.append("{} {}".format(int(value), name))
    return ', '.join(result[:granularity])

class BiddingBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='ff!',
            case_insensitive=True
        )

        for module in modules:
            try:
                self.load_extension(module)
            except Exception as e:
                print(f'Error loading module {module}:')
                print(e);
            else:
                print(f"Module {module} loaded successfully")

    async def send(self, *args, **kwargs):
        return await self.sender(*args, **kwargs)

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(name="Football!", type=discord.ActivityType.watching))

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            ctx.send(embed=discord.Embed(
                title='Woah! Slow down!',
                description=f'You can runt his command again in {display_time(error.retry_after)}',
                color=discord.Color.red()
            ))
        elif hasattr(error, 'Embed'):
            await ctx.send(embed=error.Embed)
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send(embed=discord.Embed(
                title='I don\'t have permissions to do that!',
                description='Change my permissions to retry',
                color=discord.Color.red()
            ))
        elif isinstance(error, commands.CommandNotFound):
            return
        else:
            await ctx.send(embed=discord.Embed(title=error.__class__.__name__, description=str(error), color=discord.Color.red()))



bot = BiddingBot()

load_dotenv()
bot.run(os.getenv('TOKEN'))