from discord.ext import commands
import discord
import json

class footballAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bid(self, ctx, amount:int, *, player:str):
        with open('Cogs/data.json', 'r') as data_file:
            data = json.loads(data_file.read() or '{}')
            oldamount = 0
            if not str(ctx.author.id) in data:
                data[str(ctx.author.id)] = {player.lower(): amount}
            else: 
                oldamount = data[str(ctx.author.id)].get(player.lower()) or 0
                data[str(ctx.author.id)].update({player.lower(): amount})
            data_file.close()

        with open('Cogs/data.json', 'w') as data_file:    
            data_file.write(json.dumps(data, indent=4))
            data_file.close()
  
        return await ctx.send(embed=discord.Embed(title='Success!', description=f"Changed your bid of {player} from {oldamount} to {amount}", color=discord.Color.green()))

    @commands.command(aliases=['cc'])
    async def createchannel(self, ctx):
        for channel in ctx.guild.text_channels:
            if channel.name == str(ctx.author.id):
                return await ctx.send(embed=discord.Embed(title='Failure!', description=f"Channel <#{channel.id}> already created!", color=discord.Color.red()))
        guild = ctx.guild
        member = ctx.author
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            member: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await ctx.guild.create_text_channel(str(ctx.author.id), overwrites=overwrites)
        return await ctx.send(embed=discord.Embed(title='Success!', description=f"Channel <#{channel.id}> created!", color=discord.Color.green()))

    @commands.command()
    async def get(self, ctx):
        for channel in ctx.guild.text_channels:
            if channel.name == str(ctx.author.id):
                with open('Cogs/data.json', 'r') as data_file:
                    data = json.loads(data_file.read() or '{}')
                    if not str(ctx.author.id) in data:
                        await channel.send(embed=discord.Embed(title='No Bids!', description=f"You have no bids!", color=discord.Color.red()))
                        return await ctx.send(embed=discord.Embed(title='Success!', description=f"Bids sent to <#{channel.id}>!", color=discord.Color.green()))
                    else:
                        bids = dict(data.get(str(ctx.author.id)))
                        for k in bids:
                            await channel.send(embed=discord.Embed(title='Bid!', description=f"Your bid for {k} is {bids[k]}!", color=discord.Color.green()))
                        return await ctx.send(embed=discord.Embed(title='Success!', description=f"Bids sent to <#{channel.id}>!", color=discord.Color.green()))
        return await ctx.send(embed=discord.Embed(title='Failure!', description=f"Please create a channel first using `ff!cc`!", color=discord.Color.red()))

setup = lambda bot:bot.add_cog(footballAPI(bot))