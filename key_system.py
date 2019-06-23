import sys
import discord
from discord.ext import commands
import string
import random
import json
from itertools import chain
from datetime import datetime
import re
client = commands.Bot(command_prefix = ".")

TOKEN = "NTM3NDE2MTk4NjQ4ODg5MzY5.XLeaPQ.jloSfJ7LIXAwkWrsxyKvfWF6aEQ"
guild_id = 487880066630680587
admin_channel=[577008065262518292]




non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def key_gen():
    keylist= [random.choice(string.ascii_uppercase) for i in range(5)]
    return ("SKR"+"".join(keylist))

def recover_user(dicty,value):
    for a_key in dicty.keys():
        if (dicty[a_key] == value):
            return a_key

print("----------------------------------"+str(datetime.now().strftime("%x %H:%M"))+"----------------------------------")
print("key_system.py Loading.....")
keydict={}
try:
    file = open("keys.txt","r+") 
    keys = file.read()
    keydict = json.loads(keys)
    file.close()
except:
    print("Error: keys.txt cannot be opened!")
    print("Exiting Program........")
    sys.exit()
print("Bot is ready.")

@client.event
async def on_ready():
    print("----------------------------------"+str(datetime.now().strftime("%x %H:%M"))+"----------------------------------")
    print("Checking if all existing members have a unique key")
    guild = client.get_guild(guild_id)
    for m in guild.members:
        if (str(m.id) not in keydict.keys()):
            keydict[str(m.id)]=key_gen()

        while True:
            rev_dict = {} 
            for key, value in keydict.items(): 
                rev_dict.setdefault(value, set()).add(key) 
      
      
            dup_key = set(chain.from_iterable( 
                 values for key, values in rev_dict.items() 
                 if len(values) > 1))
            dup_key = list(dup_key)
            if (len(dup_key)==0):
                break
            print("Duplicate Key Found!")
            keydict[str(m.id)]=key_gen()
            print("Key Reassigned!")

    with open('keys.txt', 'w') as file:
        file.write(json.dumps(keydict))
    file.close()
    print("All existing members have a unique key NOW")
    print("Key System Initialization is Done")


@client.event
async def on_member_join(member):
    print("----------------------------------"+str(datetime.now().strftime("%x %H:%M"))+"----------------------------------")
    print (str(message.author.id).translate(non_bmp_map)+" join in the Server. Generating key...")
    try:
        file = open("keys.txt","r+") 
        keys = file.read()
        keydict = json.loads(keys)
        file.close()
    except:
        print("Error: keys.txt cannot be opened!")
        return
    if (str(member.id) not in keydict.keys()):
        keydict[str(member.id)]=key_gen()

        while True:
            rev_dict = {} 
            for key, value in keydict.items(): 
                rev_dict.setdefault(value, set()).add(key) 
      
      
            dup_key = set(chain.from_iterable( 
                 values for key, values in rev_dict.items() 
                 if len(values) > 1))
            dup_key = list(dup_key)
            if (len(dup_key)==0):
                break
            keydict[str(member.id)]=key_gen()

    with open('keys.txt', 'w') as file:
        file.write(json.dumps(keydict))
    file.close()

@client.event
async def on_message(message):
    channel_id=message.channel.id
    guild = client.get_guild(guild_id)
    if message.content.lower().startswith("!key"):
        print("----------------------------------"+str(datetime.now().strftime("%x %H:%M"))+"----------------------------------")
        print (message.author.name.translate(non_bmp_map)+"#"+message.author.discriminator+" "+str(message.author.id)+" sent a request for key")
        try:
            file = open("keys.txt","r+") 
            keys = file.read()
            keydict = json.loads(keys)
            file.close()
        except:
            print("Error: keys.txt cannot be opened!")
            return
        user= str(message.author.id)
        await message.author.send("Your key is: "+keydict[user])
        print ("Key sent!")
        return

    if message.content.lower().startswith("!searchkey"):
        print("----------------------------------"+str(datetime.now().strftime("%x %H:%M"))+"----------------------------------")
        print (message.author.name.translate(non_bmp_map)+"#"+message.author.discriminator+" "+str(message.author.id)+" sent a request for User Information")
        try:
            file = open("keys.txt","r+") 
            keys = file.read()
            keydict = json.loads(keys)
            file.close()
        except:
            print("Error: keys.txt cannot be opened!")
            return
        key_info= str(message.content[11:])
        if len(key_info)!=8:
            await message.channel.send("Error: Key Length Should be 8 digits. SKRXXXXX")
            print ("Error: Key Length Should be 8 digits. SKRXXXXX")
            return
        print ("Searching who is having key: "+ key_info)
        user_id = recover_user(keydict,key_info)
        if user_id is None:
            message.channel.send("No User is obtaining the key: "+ key_info)
            print("No User is obtaining the key: "+ key_info)
            return
        for m in guild.members:
            if (str(m.id)== user_id) and (channel_id in admin_channel):
                print (m.name+"#"+m.discriminator+" User ID: "+str(m.id))
                await message.channel.send("The information of Key Owner: "+key_info)
                await message.channel.send("Discord Name: "+m.name+"#"+m.discriminator)
                await message.channel.send("User ID: "+str(m.id))
                return
        print ("Key Owner not found")
        #await message.author.send("Your key is: "+keydict[user])
        #print ("Key sent!")
        return
    return
    

client.run(TOKEN)
