import main as m
import discord
from discord.ext import  tasks
import connection as c
import slash

# On ready
@m.client.event
async def on_ready():
  print("Bot is ready")
  servers = len(m.client.guilds)
  await m.client.tree.sync()
  c.connect()
  check_last.start()
  await m.client.tree.sync()
  
  await m.client.change_presence(
    activity=discord.Activity(type=discord.ActivityType.watching,
                              name=f'{servers} Servers 🍭'))

# ON JOIN SERVER
@m.client.event
async def on_member_join(member):
  # check server id and channel id
  check = c.checkwelcome(member.guild.id)
  if(len(check) != 0):
     channel = m.client.get_channel(int(check[0][3]))
     embed = discord.Embed(title="Announcement", description="```diff\n+Welcome To This Server```", color=0x00ff00)
     embed.add_field(name="Message", value=f"{check[0][1]} {member.mention} to {member.guild.name} ! 🎉", inline=False)
     embed.set_thumbnail(url=member.avatar)
     embed.add_field(name="User ID", value=member.id, inline=True)
     embed.set_footer(text=f"You're the {member.guild.member_count} member")
     await channel.send(embed=embed) 

# ON LEAVE SERVER
@m.client.event
async def on_member_remove(member):
  check = c.checkwelcome(member.guild.id)
  if(len(check) != 0):
     channel = m.client.get_channel(int(check[0][3]))    
     embed = discord.Embed(title="Announcement", description="```diff\n-Leave This Server```", color=0xff0000)
     embed.add_field(name="Message", value=f"{member.mention} Just Left {member.guild.name} ! ♿️", inline=False)
     embed.set_thumbnail(url=member.avatar)
     embed.add_field(name="User ID", value=member.id, inline=True)
     embed.set_footer(text=f"The current number of members is {member.guild.member_count} ")
     await channel.send(embed=embed) 
   


# ON MESSAGE IN BOT SERVER
@m.client.event
async def on_message(message):
  # get message after >last
  pesan = message.content.split(" ")
  # add last request
  if(pesan[0].lower() == ">last"):
    # check permission user 
    if(message.author.guild_permissions.administrator):
        # check server id and channel id
        if(c.checkserver(message.guild.id) ==False or c.checkchannel(message.guild.id,message.channel.id) ==False):
           embed = discord.Embed(title="Error", description="You have been request before or Limit", color=0xff0000)
           await message.channel.send(embed=embed, reference = message, delete_after=10)
        else:
          req_message = message.content[6:len(message.content)]
          if(len(pesan)==1):
              await message.channel.send("Please input `Request Message`", reference = message, delete_after=10)
          else:

             embed = discord.Embed(title="Success", description="Your request has been sent", color=0x00ff00)
             mess = await message.channel.send(embed=embed, reference = message, delete_after=10)
             data = {
                "req_message":req_message,
                "server_id":message.guild.id,
                "channel_id":message.channel.id,
                "message_id":mess.id
             }
             c.insert_last(data)
    else:
        embed = discord.Embed(title="Error", description="You don't have permission", color=0xff0000)
        await message.channel.send(embed=embed, reference = message, delete_after=10)

  # delete last request 
  elif(pesan[0].lower() == ">del"):
      # check pesan[1] is last
      if(pesan[1].lower() == "last"):
        # check permission user
        if(message.author.guild_permissions.administrator):
          if(c.checkchannel(message.guild.id,message.channel.id) == False):
            #  delete last request
            temp = c.get_one_last(message.guild.id,message.channel.id)
            if(c.delete_last(message.guild.id,message.channel.id) == True):
              # delete message_id
              channel = m.client.get_channel(message.channel.id)
              await channel.delete_messages([discord.Object(id=temp[0][4])])
              embed = discord.Embed(title="Success", description="Your request has been deleted", color=0x00ff00)
              await message.channel.send(embed=embed, reference = message, delete_after=10)
          else:
             embed = discord.Embed(title="Error", description="You don't have request for this channel", color=0xff0000)
             await message.channel.send(embed=embed, reference = message, delete_after=10)
        else:
          embed = discord.Embed(title="Error", description="You don't have permission", color=0xff0000)
          await message.channel.send(embed=embed, reference = message, delete_after=10)
      else:
          embed = discord.Embed(title="Error", description="Invalid Commands, only available `>del last`", color=0xff0000)
          await message.channel.send(embed=embed, reference = message, delete_after=10)
         
  # welcome message to turn on 
  elif(pesan[0].lower() == ">welcome"):
    if(len(pesan) != 1):
      if(pesan[1].lower() == "on"):
          if(message.author.guild_permissions.administrator):
            #  check channel id and server id
            check_server = c.checkwelcome(message.guild.id)
            if(len(check_server) == 0):
              if(len(pesan) == 2):
                data = {
                  "req_message": "Welcome",
                  "server_id":message.guild.id,
                  "channel_id":message.channel.id,
                  "w_status" : "on"
                }
                c.insert_welcome(data)
                embed = discord.Embed(title="Success", description="Welcome Message has been turn on 🌿", color=0x00ff00)
                await message.channel.send(embed=embed, reference = message, delete_after=10)
              else:
                data = {
                    "req_message": message.content[11:len(message.content)],
                    "server_id":message.guild.id,
                    "channel_id":message.channel.id,
                    "w_status" : "on"
                } 
                c.insert_welcome(data)
                embed = discord.Embed(title="Success", description="Welcome Message has been turn on 🌿", color=0x00ff00)
                await message.channel.send(embed=embed, reference = message, delete_after=10)
            else:
              embed = discord.Embed(title="Error", description=f"Your Server Already Active on {m.client.get_channel(int(check_server[0][3])).mention}", color=0xff0000)
              await message.channel.send(embed=embed, reference = message, delete_after=10)        
               
          else:
            embed = discord.Embed(title="Error", description="You dont Have `Permissions Server` For This Command", color=0xff0000)
            await message.channel.send(embed=embed, reference = message, delete_after=10)        
      elif(pesan[1].lower() == "off"):
          if(message.author.guild_permissions.administrator):
            #  check channel id
            check_server = c.checkwelcome(message.guild.id)
            if(len(check_server) == 1):
              c.delete_welcome(message.guild.id)
              embed = discord.Embed(title="Success", description="Welcome Message has been turn off 🍂", color=0x00ff00)
              await message.channel.send(embed=embed, reference = message, delete_after=10)
            else:
              embed = discord.Embed(title="Error", description="Invalid Request, Your server Haven't activated before", color=0xff0000)
              await message.channel.send(embed=embed, reference = message, delete_after=10)
          else:
            embed = discord.Embed(title="Error", description="You don't have `Permissions Server` For This Command ", color=0xff0000)
            await message.channel.send(embed=embed, reference = message, delete_after=10)
             
      else:
          embed = discord.Embed(title="Error", description="Invalid Commands, only available `>welcome on` or `>welcome off` 🔥", color=0xff0000)
          await message.channel.send(embed=embed, reference = message, delete_after=10)
    else:
            embed = discord.Embed(title="Error", description="Invalid Commands, only available `>welcome on` or `>welcome off` ✨", color=0xff0000)
            await message.channel.send(embed=embed, reference = message, delete_after=10)
  elif(pesan[0].lower() == ">help"):
     embed = discord.Embed(title= "List Commands 🍀" , description="```diff\n+Yo!```" , color=0x00ffdd)
     embed.set_thumbnail(url=m.client.user.display_avatar.url)
     embed.add_field(name=f"Informatin About {m.client.user.name}", value= "Since 2023 By ERHA 🌿", inline=False)
     embed.add_field(name="Prefix", value="`>`", inline=False)
     embed.add_field(name="last <req_message>", value="For `Create` a custom message always displayed at the bottom of a channel. \n```Example: >last HALO```", inline=False)
     embed.add_field(name="del <options>", value="For `Delete` a custom message always displayed at the bottom of a channel. The available options are `last` \n```Example: >del last```", inline=False)
     embed.add_field(name="welcome <options>", value="For `Turn On` or `Turn Off` a welcome message when a new member joins the server. The available options are `on` or `off` \n```Example: >welcome on```", inline=False)
     embed.add_field(name="invite", value="For `Invite` me to your server \n```Example: >invite```", inline=False)
     temp = "{/}"
     embed.set_footer(text=f"{m.client.user.name} Supports Commands Slash {temp} 💖")
     await message.channel.send(embed=embed, reference = message)
  elif(pesan[0].lower() == ">invite"):
     link = "https://discord.com/api/oauth2/authorize?client_id=1101357310816829510&permissions=8&scope=bot"
     embed = discord.Embed(title="Invite Me", description=f"[Click Here]({link})", color=0x00ff00)
     await message.channel.send(embed=embed , reference = message)

         
# loop for check last request
@tasks.loop(seconds=5)
async def check_last():
   autor_id = m.client.user.id
   all_data = c.get_all_last()
   for data in all_data:
        # print(data)
        channel = m.client.get_channel(int(data[3]))
        # get autor id last message in channel
        last_mess = channel.last_message_id
        # last_mess =await channel.fetch_message(channel.last_message_id)
        try:
          # if(last_mess.author.id != autor_id):
          if(str(last_mess) != data[4]):
            await channel.delete_messages([discord.Object(id=int(data[4]))])
            mess = await channel.send("__**ChikaBot ちか  Message:**__\n"+data[1])
            c.update_last(data[0],mess.id)
          else:
            pass
        except Exception as e:
            pass           
# GET TOKEN
# get token from .env file in same directory
m.client.run("")