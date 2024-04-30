import disnake
from disnake.ext import commands

async def embed_test():
    embed = disnake.Embed(
        title="Weekly IO Update",
        color=0x40e0d0 #TURQUOISE
	)
    embed.add_field(name="Current Lead", value="Test Value", inline=False)
    embed.add_field(name="Most IO gained this week", value="Test Value 2", inline=False)
    embed.add_field(name="Top 5", value="Person1\nPerson2\nPerson3\nPerson4\nPerson5", inline=False)
    embed.set_footer(text="Good luck IO Hunting this week!")
    return(embed)
    
class EmbedCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Test an Embed.")
    async def embed_test(self, inter: disnake.ApplicationCommandInteraction):
        #This 
        await inter.response.send_message(embed=(await embed_test()))

def setup(bot: commands.Bot):
    bot.add_cog(EmbedCommand(bot))