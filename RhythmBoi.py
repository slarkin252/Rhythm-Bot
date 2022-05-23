import discord
import random
import json
import asyncio
import os
import youtube_dl
import shutil
from itertools import cycle
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext.commands import Bot
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient


client = commands.Bot(command_prefix = '!')

def is_it_me(ctx):
    return ctx.author.id == 231947797409038336

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(executable = 'C:\\ffmpeg.exe', source = filename, **ffmpeg_options), data=data)


@client.event
async def on_ready():
    global onReadyStatus
    onReadyStatus = 'Mf Risk of Rain 2 Beetle'
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(onReadyStatus))
    #change_status.start()
    pfp_path = "C://Users//User//Pictures//RoR2Beetle.png"

    fp = open(pfp_path, 'rb')
    pfp = fp.read()
    await client.user.edit(avatar=pfp)
    print('Bot is ready.')

def __init__(self, bot):
        self.bot = bot

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('This command does not exist.')


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

"""
@clear.error
async def clear_error(ctx, error):
if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify how many errors you want to clear.')
"""     
"""------------------------------------------------------------------- """

#join a specific voice channel without being in it
@client.command(aliases= ['RhythmBombing','joinS','joins'])
async def joinSpecific(ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        
        if ctx.voice_client is not None:
            print("I'm in")
            return await ctx.voice_client.move_to(channel)
        print(channel)
        await channel.connect()
        print('await is actually working')
        



#***working join***
@client.command(pass_context=True,aliases=['join','Join'])
async def joinVC(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)
    voice = ctx.message.author.voice
    print(channel, voice)
       
    """
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        print ("not channel")
        #return
    """  
    
    if voice and voice.is_connected():
        print ("if")
        await voice.move_to(channel)
        print("passed first await")
        await ctx.send("Joining now.")
    else:
        print ("else")
        voice = channel.connect()
        await ctx.send("Can't join.")
    #source = FFmpegPCMAudio('1.m4a')
    #player = voice.play(source)

@client.command
async def joinBS(ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel and stolen directly from Actually Stolen.py"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
        
        
#***join for General specifically***
@client.command(pass_context=True,aliases=['goToTheGeneralAndSaveSomeTime','GTTGASST', 'joinG'])
async def joinGeneral(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild) 
    print(channel, voice)
    await voice.move_to(channel)
    print("passed first await")
    await ctx.send("Joining now.")
    

#leave
@client.command(pass_context=True, aliases = ['disconnect','dismiss','stop'])
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    await voice_client.disconnect()

"""
#play command!!!

@client.command(pass_context=True)
async def play(ctx, url):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    player = await ytdl(url)
    players[guild.id] = player
    player.start()
"""

"""
@client.command(pass_context=True)
async def yt(ctx):
        url = ctx.message.content
        print(url)
        url = url.strip('!yt ')
        print(url)

        author = ctx.message.author
        print(author)
        voice_channel_ = author.voice.channel
        print(voice_channel_)
        vc = await channel.connect(voice_channel_)
        print("past vc variable setup")
        await channel.connect(voice_channel_)
        print("past actually joining but something just dont work")

        player = await vc.create_ytdl_player(url)
        player.start()
        
"""

#almost working play command!!!

@client.command(pass_context=True)
@commands.check(is_it_me)
async def Play(ctx, *, url):
    #Plays from a url (almost anything youtube_dl supports)
        async with ctx.typing():
            print('enter the asyncgeon')
            #player = await YTDLSource.from_url(url, loop=client.loop)
            player = await YTDLSource.from_url(url, loop=bot.loop)
            print("Trying to play lonk")
            ctx.message.guild.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))


@client.command(aliases = ['play', 's'])
async def stream(ctx, *, url):
    """Streams from a url (same as yt, but doesn't predownload)"""
    #primary play function

    async with ctx.typing():
        print('enter the async')
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        print(url)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        print('Should be working in full')

    await ctx.send('Now playing: {}'.format(player.title))
    
    
@client.command(aliases = ['filePlay','fileStream', 'playdl', 'filesearch'])
async def fileSearch(ctx, *, query):
    """Plays a file from the local filesystem"""

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('Now playing: {}'.format(query))


@client.command(aliases = ['filelist'])
async def fileList(ctx):
    #gives file list
    global fileList
    fileList = 'con lentitud poderosa.webm, Elevator Music.webm, La Vie en Rose.webm, Todd Howard Song.webm, Yung Gravy Oops.m4a, FunkyMonkeyFriday.m4a'
    print(fileList)
    await ctx.send(fileList)
    


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball','test','Magic8ball','MagicConch'])
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Don\'t count on it.',
                 'It is certain.',
                 'I have spoken.',
                 'Nah fam.',
                 'You gucci.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    
#clear for only those with permission
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 10):
    await ctx.channel.purge(limit = amount)

#gives a starting command list
@client.command(aliases = ['commands','HowDo','commandlist'])
async def commandList(ctx):
    await ctx.send(onReadyStatus)
    await ctx.send('Commands will sometimes have a slash \'/\' to indicate other names to call the command')
    #in onready command (@ top for Beeg and bottom for stolen)
    await ctx.send('To play music: use !joinSpecific General or whatever VC you want, then !play https://www.youtube.com/watch?v=dQw4w9WgXcQ or whatever the video link is')
    await ctx.send('In order to work, must not be in chat, then invited to join, then play one song, then leave, then repeat for now')
    await ctx.send('Current: joinSpecific/joinS(joins a specified chat), stream/play(plays a youtube video AFTER joining VC), clear(clears 10 or however many are specified), leave/disconnect(leaves), commandList(gives this list of commands), ping, 8ball, example, hello, helloThere and that\'s about it for now')
    await ctx.send('In Progress: fileSearch(plays a specific predownloaded file), join(joins your current channel), joinGeneral(joins General), improve consistency and autojoin upon summon')

@client.command(aliases = ['I_Have_The_Power','IAmTheSenate'])
#@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'I am the senate.\nDarth {ctx.author}')
    
@client.command()
async def hello(ctx):
    await ctx.send("Hello there")

@client.command()
async def helloThere(ctx):
    await ctx.send("General Kenobi")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

client.run('*********************') #reinsert the token to run properly
