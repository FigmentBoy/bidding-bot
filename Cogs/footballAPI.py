from discord.ext import commands
import discord
import json
import asyncio

class footballAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bid(self, ctx, amount:int, *, player:str):
        if ctx.channel.name != str(ctx.author.id):
            await ctx.message.delete()
            raise commands.PrivateMessageOnly(message='You can\'t run this command outside of your own private message! The command you typed is being deleted for secrecy')

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

    @commands.command(aliases=['dc'])
    async def deletechannel(self, ctx):
        for channel in ctx.guild.text_channels:
            if channel.name == str(ctx.author.id):
                if ctx.channel.id != channel.id:
                    await channel.delete()
                    return await ctx.send(embed=discord.Embed(title='Success!', description=f"Your private channel has been deleted!", color=discord.Color.green()))
                else:
                    await channel.delete()
                    return
        return await ctx.send(embed=discord.Embed(title='Failure!', description=f"You don't have a private channel! Do `ff!cc` to create one", color=discord.Color.red()))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def get(self, ctx):
        string = ""
        with open('Cogs/data.json', 'r') as data_file:
            data = json.loads(data_file.read() or '{}')
            data_file.close()
            for member in ctx.guild.members:
                print(member.id)
                mdata = data.get(str(member.id)) or None
                for channel in ctx.guild.text_channels:
                    if channel.name == str(ctx.author.id):
                        await channel.delete()
                if mdata:
                    for k in dict(mdata):
                        string += f'Bid by {member.name}#{member.discriminator} for `{k}`: `{dict(mdata)[k]}`\n'
        
        with open('Cogs/data.json', 'w') as data_file:    
            data_file.write(json.dumps({}, indent=4))
            data_file.close()

        n = 4000
        strings = [string[i:i+n] for i in range(0, len(string), n)]

        for s in strings:
            await ctx.send(s)

setup = lambda bot:bot.add_cog(footballAPI(bot))