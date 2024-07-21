import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = self.bot.settings.get('reactionRolesChannel')
        self.reaction_roles = self.bot.settings.get('reactionRolesDictionary')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        message_id = payload.message_id
        user_id = payload.user_id
        emoji = str(payload.emoji)
        print(f"emoji: {emoji}")

        # Fetch the channel and message
        channel = self.bot.get_channel(channel_id)
        if not channel:
            logger.warning(f'Channel ID {channel_id} not found.')
            return
        
        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            logger.warning(f'Message ID {message_id} not found.')
            return

        user = self.bot.get_user(user_id)
        if not user:
            logger.warning(f'User ID {user_id} not found.')
            return

        # Check if the reaction is for the correct message
        print(f"{message.id} | {self.bot.settings.get('reactionMessageId')}")
        if message.id == self.bot.settings.get('reactionMessageId'):
            #print(f"dictionaryEntryCheck: {self.reaction_roles.get(emoji)}")
            check = "official" if(emoji == '🟦') else "unofficial"
            rolename = self.reaction_roles.get(check)
            role = discord.utils.get(message.guild.roles, name=rolename)
            if role:
                member = message.guild.get_member(user_id)
                if member:
                    try:
                        await member.add_roles(role)
                        logger.info(f'Role {role} assigned to {member}.')
                    except discord.Forbidden:
                        logger.error('Insufficient permissions to add roles.')
                    except discord.HTTPException as e:
                        logger.error(f'Error adding role: {e}')
                else:
                    logger.warning(f'Member ID {user_id} not found in the guild.')
            else:
                logger.warning(f'Role "YourRoleName" not found.')
        else:
            logger.info(f'Reaction on message ID {message_id} is not configured.')
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel_id = payload.channel_id
        message_id = payload.message_id
        user_id = payload.user_id
        emoji = str(payload.emoji)

        # Fetch the channel and message
        channel = self.bot.get_channel(channel_id)
        if not channel:
            logger.warning(f'Channel ID {channel_id} not found.')
            return
        
        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            logger.warning(f'Message ID {message_id} not found.')
            return

        user = self.bot.get_user(user_id)
        if not user:
            logger.warning(f'User ID {user_id} not found.')
            return

        # Check if the reaction is for the correct message
        if message.id == self.bot.settings.get('reactionMessageId'):
            check = "official" if(emoji == '🟦') else "unofficial"
            rolename = self.reaction_roles.get(check)
            role = discord.utils.get(message.guild.roles, name=rolename)
            if role:
                member = message.guild.get_member(user_id)
                if member:
                    try:
                        await member.remove_roles(role)
                        logger.info(f'Role {role} removed from {member}.')
                    except discord.Forbidden:
                        logger.error('Insufficient permissions to add roles.')
                    except discord.HTTPException as e:
                        logger.error(f'Error removing role: {e}')
                else:
                    logger.warning(f'Member ID {user_id} not found in the guild.')
            else:
                logger.warning(f'Role "YourRoleName" not found.')
        else:
            logger.info(f'Reaction on message ID {message_id} is not configured.')

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
