import re
import numpy as np
import time
import pickle
import schedule

from discord import Embed, Role, utils
from discord.ext import commands, tasks

from utility import get_message_embed
from constants import still_alive

class ConfigInfo:

    def __init__(self, post_channel=None, guild_id=0):
        self.post_channel = post_channel
        self.guild_id = guild_id

    def __init__(self, d):
        self.post_channel = d['post_channel']
        self.guild_id = d['guild_id']

    def load_info(self, d={"0":0}):
        self.post_channel = d['post_channel']
        self.guild_id = d['guild_id']

    def load_info(self, fname=""):
        with open(fname, 'lb') as f:
            d = pickle.load(f)
        self.post_channel = d['post_channel']
        self.guild_id = d['guild_id']

    def store_info(self, fname):
        d = {'post_channel': self.post_channel,
             'guild_id': self.guild_id}
        with open(fname, 'wb') as f:
            pickle.dump(d, f)




class ScheduledMessagingCog(commands.Cog, name="ScheduledMessagingCog"):

    def __init__(self, bot, helpcommand):
        self.bot = bot
        self.__original_help_command = bot.help_command
        bot.help_command = helpcommand
        bot.help_command.cog = self

        self.postchannel = ""

        self.info = ConfigInfo()

        self.sing_every_hour.start()
    # =============== USER COMMANDS

    @staticmethod
    def has_role(ctx, role):
        coordinator_role = utils.find(lambda r: r.name == role, ctx.guild.roles)
        return coordinator_role in ctx.author.roles

    @staticmethod
    def is_team_member(ctx):
        coordinator_role = utils.find(lambda r: r.name == 'Team', ctx.guild.roles)
        return coordinator_role in ctx.author.roles

    @commands.command('template',
                        aliases = [ 't' , 'tmp' ],
                        help = "Template for bot command",
                        usage = '')
    async def template(self, ctx, *, args):

        user_id = ctx.author.id
        user_name = ctx.author.display_name

        emb = get_message_embed(ctx, f"Called by {user_name}")

        await ctx.send(embed = emb)


    @commands.command("set_birdie_free")
    @commands.has_role("BirdPeeper")
    async def set_post_channel(self, ctx):
        f = open("postpickle", "wb")
        self.postchannel = ctx.channel
        pickle.dump(ctx.channel.id, f)
        f.close()

        await self.postchannel.send("_Takes flight_")
        await self.postchannel.trigger_typing()
        time.sleep(2)
        await self.postchannel.send("**SWEET FREEDOM!!**")


    @commands.command("post_message")
    @commands.has_role("BirdPeeper")
    async def post_message(self, ctx):
        try:
            await self.postchannel.send(content="This is working! Yay, birbs!")
            time.sleep(3)
            await self.postchannel.send("I'm gonna fucking do it again!")
            time.sleep(3)
            await self.postchannel.send(content="This is working! Yay, birbs!")
        except:
            await ctx.send("Show me where I should fly to, to spread this message?")


    @commands.command("sing_the_song_of_our_people")
    @commands.has_role("BirdPeeper")
    async def sing_alive(self, ctx):
        f = open("postpickle", "rb")
        ch = ctx.guild.get_channel(pickle.load(f))
        f.close()

        lastLineEmpty = False
        for line in still_alive:
            if line == "":
                time.sleep(2)
                await ch.send("** **")
                lastLineEmpty = True
            else:
                await ch.trigger_typing()
                time.sleep(1)
                if lastLineEmpty == True:
                    await ch.send(line)
                else:
                    await ch.send(line)
                lastLineEmpty = False

    @tasks.loop(minutes=1)
    async def sing_every_hour(self):
        # f = open("postpickle", "rb")
        # ch = ctx.guild.get_channel(pickle.load(f))
        # f.close()
        # await ch.send("Chirp")
        #------------------------------------------------------- ?!
        self.fetch_guild(self.guild_id)
        print("Chirp")


    # @commands.command('no_arg')
    # async def no_args(self, ctx):
    #     print("no Arguments!")
    #
    # # Tuple of values, space separated
    # @commands.command('multi_arg')
    # async def multi_arg(self, ctx, *args):
    #     print(f"{args}")
    #
    # # A single string
    # @commands.command('one_arg')
    # async def one_arg(self, ctx, *, args):
    #     print(f"{args}")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        self.bot.write_error(f"{repr(error)}", ctx.message)

        print(error)

        if isinstance(error, commands.errors.CheckFailure):
            luck = np.random.random()
            if luck < 0.3:
                await ctx.send("IGNORE") #You don't have the permissions to do this
            elif luck < 0.6:
                await ctx.send("Nope, not for you")
            else:
                await ctx.send("_Flies away from the unworthy_")
        elif "ValueError" in repr(error):
            await ctx.send("Arguments incorrectly formatted, check lb_help for info")
        elif "BadArgument" in repr(error):
            await ctx.send("Incorrect argument format, check lb_help for info")
        else:
            await ctx.send(error)
