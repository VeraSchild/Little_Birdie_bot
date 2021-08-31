# Simple class for storing and loading configuration info
# about guild id's and post channel id's
class ConfigInfo:

    def __init__(self, post_channel=None, guild_id=0):

        self.post_channel = post_channel
        self.guild_id = guild_id

        self.__to_dict()

    ###################################### SETTERS
    def set_info(self, d={"0":0}):
        self.post_channel = d['post_channel']
        self.guild_id = d['guild_id']

        self.__to_dict()

    def set_post_channel(self, post_channel):
        self.post_channel = post_channel

        self.__to_dict()

    def set_guild_id(self, guild_id):
        self.guild_id = guild_id

        self.__to_dict()

    ###################################### GETTERS
    def get_dict(self):
        return self.dict
    
    def get_post_channel(self):
        return self.post_channel

    def get_guild_id(self):
        return self.guild_id

    # Call from bot with 'ConfigInfo.get_guild(this)'
    def get_guild(self, bot):
        return bot.get_guild(self.guild_id)
    
    # Call from bot with 'ConfigInfo.get_post_channel(this)'
    def get_post_channel(self, bot):
        return bot.get_channel(self.post_channel)

    ###################################### PICKLE METHODS
    # Load from file
    def load_info(self, fname=""):

        with open(fname, 'lb') as f:
            d = pickle.load(f)
        self.post_channel = d['post_channel']
        self.guild_id = d['guild_id']

        self.__to_dict()

    # Store to file
    def store_info(self, fname):

        d = {'post_channel': self.post_channel,
             'guild_id': self.guild_id}
        with open(fname, 'wb') as f:
            pickle.dump(d, f)

    def __to_dict(self):
        self.dict = {'post_channel': self.post_channel, 'guild_id': self.guild_id}
