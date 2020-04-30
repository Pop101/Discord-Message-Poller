# -*- coding: cp1252 -*-
import discord
from discord.ext import commands
import os, sys
import collections
from operator import attrgetter
  
MsgResponse = collections.namedtuple('MsgResponse',['message','response','time']) 
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    str(bot.user.id)
    print('Logged in as: ')
    print(bot.user.name)
    print('\nBeginning Poll:')
    text_channels = []
    for channel in bot.private_channels:
        text_channels.append(channel)
    for server in bot.guilds:
        for channel in server.text_channels:
            text_channels.append(channel)
    
    allMessages = []
    for channel in text_channels:
        messages = await channel.history(oldest_first=False).flatten()
        i = -1;
        while i+1 < len(messages):
            i += 1
            message = messages[i]

            # ignore the message if it isn't from the bot
            if message.author.id != bot.user.id:
                continue;
            
            # get response (its first)
            response = ""
            while i < len(messages) and messages[i].author.id == bot.user.id:
                response = str(messages[i].content) + "\n" + response
                i += 1

            # if you sent the first message
            if i >= len(messages):
                continue
            
            # get other person's idea
            otherID = messages[i].author.id            
            query = ""
            while i < len(messages) and messages[i].author.id == otherID:
                query = str(messages[i].content) + "\n" + query
                i += 1
            i -= 1

            
            query = query.lstrip()
            response = response.lstrip()
            print('found message '+response+' after '+query)
            if len(query) > 3 and len(response) > 3:
                allMessages.append(MsgResponse(query, response, message.created_at))
                with open('data.txt', 'a', encoding="utf-8") as file:
                    file.write('<startmsg>\n'+query+'\n'+response) 

    # Sort by date created
    allMessages = sorted(allMessages, key=attrgetter('time'))
    # Overwrite the old list with the sorted list
    with open('data.txt', 'w', encoding="utf-8") as file:
        for msg in allMessages:
            file.write('<startmsg>\n'+msg.message+'\n'+msg.response) 
    # Now exit
    await ctx.bot.logout()
    sys.trackbacklimit=None
    sys.exit(0)
    
print('Enter token ( you can get yours via https://discordhelp.net/discord-token ):')
token = str(input())
print('Connecting to discord...')
bot.run(token,bot=False)

