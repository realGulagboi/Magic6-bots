import discord
from discord.ext import commands
import json
import utils

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='setup', help="Set up the reaction role message")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        #EMOJI = '✅'
        BLUESQUARE = '🟦'
        ORANGESQUARE = '🟧'
        message = await ctx.send('React to this message with either of the emojis to get the role.')
        await message.add_reaction(BLUESQUARE)
        await message.add_reaction(ORANGESQUARE)

        # Delete the command message
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            # Bot lacks permissions to delete the message
            await ctx.send("I don't have permission to delete messages.")
        except discord.HTTPException as e:
            # Handle other HTTP exceptions
            await ctx.send(f"An error occurred while trying to delete the command message: {e}")

        #print(f'Message ID: {message.id}')
        self.bot.settings['reactionMessageId'] = message.id
        utils.save_settings(self.bot.settings)
        print(f'Setup complete! Message ID saved as {message.id}.')

async def setup(bot):
    await bot.add_cog(Setup(bot))

