import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import pytz
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Cleanup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cleanup', help="Deletes all messages in the channel.")
    @commands.has_permissions(administrator=True)
    async def cleanup(self, ctx):
        channel = ctx.channel
        deleted = 0

        # Define the cutoff time for message deletion (14 days ago, UTC timezone-aware)
        tz_utc = pytz.UTC
        now_utc = datetime.now(tz_utc)
        cutoff_time = now_utc - timedelta(days=14)

        try:
            async for message in channel.history(limit=10000, before=now_utc):
                if message.created_at > cutoff_time:
                    # Purge messages in bulk
                    deleted_messages = await channel.purge(limit=100, before=now_utc, reason="Cleanup command")
                    deleted+= len(deleted_messages)
                    #deleted += 100
                    await asyncio.sleep(2)  # Delay to handle rate limits
                else:
                    break
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages.")
        except discord.HTTPException as e:
            if e.status == 429:  # Rate limit error
                retry_after = e.retry_after
                await ctx.send(f"Rate limit hit, retrying in {retry_after} seconds.")
                await asyncio.sleep(retry_after)
                await self.cleanup(ctx)  # Retry cleanup after waiting
            else:
                await ctx.send(f"An error occurred: {e}")
        except Exception as e:
            await ctx.send(f"Unexpected error: {e}")
        else:
            await ctx.send(f"Deleted {deleted} messages.")
            # Delete the command message
            try:
                await asyncio.sleep(5)
                await ctx.message.delete()
            except discord.Forbidden:
                # Bot lacks permissions to delete the message
                await ctx.send("I don't have permission to delete messages.")
            except discord.HTTPException as e:
                # Handle other HTTP exceptions
                await ctx.send(f"An error occurred while trying to delete the command message: {e}")

async def setup(bot):
    await bot.add_cog(Cleanup(bot))
