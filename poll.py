# -*- coding: cp1252 -*-
import discord
from discord.ext import commands
import os, sys, csv, time
import collections
from operator import attrgetter
  
MsgResponse = collections.namedtuple('MsgResponse',['message','response','time']) 
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as: ')
    print(bot.user.name)
    
    text_channels = []
    for channel in bot.private_channels:
        text_channels.append(channel)
    for server in bot.guilds:
        for channel in server.text_channels:
            text_channels.append(channel)
    print('\nBeginning Poll of '+str(len(text_channels))+' channels: ')
    allMessages = []
    for channel in text_channels:
        try:
            messages = await channel.history(oldest_first=False).flatten()
            i = -1
            while i+1 < len(messages):
                i += 1
                message = messages[i]

                # ignore the message if it isn't from the bot
                if message.author.id != bot.user.id:
                    continue
                
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

                
                query = query.strip().
                response = response.strip()
                if len(query) > 0 and len(response) > 0:
                    allMessages.append(MsgResponse(query, response, message.created_at))
                    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([time.mktime(message.created_at.timetuple()), query, response])
        except:
            pass
    
    # Sort by date created
    allMessages = sorted(allMessages, key=attrgetter('time'))
    
    # Overwrite the old list with the sorted list
    with open('data.csv', 'w', newline='', encoding='utf-8') as file:
        for msg in allMessages:
            writer = csv.writer(file)
            writer.writerow([time.mktime(msg.time), msg.message, msg.response])
    
    # Now exit
    print('Polling Successful!')
    await bot.logout()

print('Enter token ( you can get yours via https://discordhelp.net/discord-token ):')
token = str(input())
print('Connecting to discord...')
bot.run(token,bot=False)

