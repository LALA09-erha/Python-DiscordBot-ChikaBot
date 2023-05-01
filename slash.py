import main as m
import discord
import connection as c

# command for ping
@m.client.tree.command(name="ping" , description="Check bot latency")
async def ping(interaction : discord.Interaction):
  await interaction.response.send_message(f"Pong 🏓 {round(m.client.latency * 1000)} ms!", ephemeral=True)

# command for last
@m.client.tree.command(name="last" , description="Request last message")
async def last(interaction : discord.Interaction , req_message:str):
    # check permission user 
    if(interaction.user.guild_permissions.administrator):
        # check server id and channel id
        if(c.checkserver(interaction.guild_id) ==False or c.checkchannel(interaction.guild_id,interaction.channel_id) ==False):
           embed = discord.Embed(title="Error", description="You have been request before or Limit", color=0xff0000)
           await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
          if(req_message == "" or req_message == " " or req_message == None):
              embed = discord.Embed(title="Error", description="Please input `Request Message`", color=0xff0000)
              await interaction.response.send_message(embed=embed, ephemeral=True)
          else:
             embed = discord.Embed(title="Success", description="Your request has been sent", color=0x00ff00)
             await interaction.response.send_message(embed=embed)
             mess = await interaction.original_response()
             data = {
                "req_message":req_message,
                "server_id":interaction.guild_id,
                "channel_id":interaction.channel_id,
                "message_id":mess.id
             }
             c.insert_last(data)
    else:
        embed = discord.Embed(title="Error", description="You don't have permission", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# delete last request
@m.client.tree.command(name="del" , description="Delete last request")
@discord.app_commands.choices( choices=[
    discord.app_commands.Choice(name="last" , value="last")
])
async def delete(interaction:discord.Interaction, choices:discord.app_commands.Choice[str]):
   await interaction.response.defer()
   if(choices.name == "last"):
      # check permission user
        if(interaction.user.guild_permissions.administrator):
          if(c.checkchannel(interaction.guild_id,interaction.channel_id) == False):
            #  delete last request
            temp = c.get_one_last(interaction.guild_id,interaction.channel_id)
            if(c.delete_last(interaction.guild_id,interaction.channel_id) == True):
              # delete interaction_id
              channel = m.client.get_channel(int(interaction.channel_id))
              # print(channel)
              await channel.delete_messages([discord.Object(id=int(temp[0][4]))])
              embed = discord.Embed(title="Success", description="Your request has been deleted", color=0x00ff00)
              await interaction.followup.send(embed=embed, ephemeral=True)
          else:
             embed = discord.Embed(title="Error", description="You don't have request for this channel", color=0xff0000)
             await interaction.followup.send(embed=embed, ephemeral=True)
        else:
          embed = discord.Embed(title="Error", description="You don't have permission", color=0xff0000)
          await interaction.followup.send(embed=embed, ephemeral=True)
   else:
      embed = discord.Embed(title="Error", description="Please input `last`", color=0xff0000)
      await interaction.followup.send(embed=embed, ephemeral=True)

# welcome message
@m.client.tree.command(name="welcome" , description="Welcome Management Command (Only Admin)")
@discord.app_commands.choices( choices=[
  discord.app_commands.Choice(name="on" , value="on") , 
  discord.app_commands.Choice(name="off" , value="off")
  ])
async def welcome(interaction:discord.Interaction, choices:discord.app_commands.Choice[str] , mess : str=None):
    await interaction.response.defer()
    if(choices.name =="on" and interaction.user.guild_permissions.administrator):
       #  check channel id and server id
            check_server = c.checkwelcome(interaction.guild_id)
            if(len(check_server) == 0):
              if(mess == None or mess == "" or mess == " "):
                data = {
                  "req_message": "Welcome",
                  "server_id":interaction.guild_id,
                  "channel_id":interaction.channel_id,
                  "w_status" : "on"
                }
                c.insert_welcome(data)
                embed = discord.Embed(title="Success", description="Welcome Message has been turn on 🌿", color=0x00ff00)
                await interaction.followup.send(embed=embed, ephemeral=True)
              else:
                data = {
                    "req_message": mess,
                    "server_id":interaction.guild_id,
                    "channel_id":interaction.channel_id,
                    "w_status" : "on"
                } 
                c.insert_welcome(data)
                embed = discord.Embed(title="Success", description="Welcome Message has been turn on 🍃", color=0x00ff00)
                await interaction.followup.send(embed=embed,ephemeral=True)
            else:
              embed = discord.Embed(title="Error", description=f"Your Server Already Active on {m.client.get_channel(int(check_server[0][3])).mention}", color=0xff0000)
              await interaction.followup.send(embed=embed,ephemeral=True)        
    elif(choices.name =="off" and interaction.user.guild_permissions.administrator):
       #  check channel id
            check_server = c.checkwelcome(interaction.guild_id)
            if(len(check_server) == 1):
              c.delete_welcome(interaction.guild_id)
              embed = discord.Embed(title="Success", description="Welcome Message has been turn off 🍂", color=0x00ff00)
              await interaction.followup.send(embed=embed, ephemeral=True)
            else:
              embed = discord.Embed(title="Error", description="Invalid Request, Your server Haven't activated before", color=0xff0000)
              await interaction.followup.send(embed=embed, ephemeral=True)
    else:
       embed = discord.Embed(title="Error", description="You don't have permission", color=0xff0000)
       await interaction.followup.send(embed=embed, ephemeral=True)

# show help command
@m.client.tree.command(name="help" , description="Show All Command")
async def help(interaction:discord.Interaction):
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
     await interaction.response.send_message(embed=embed)

@m.client.tree.command(name="invite" , description="Invite Bot")
async def invite(interaction:discord.Interaction):
   link = "https://discord.com/api/oauth2/authorize?client_id=1101357310816829510&permissions=8&scope=bot"
   embed = discord.Embed(title="Invite Me", description=f"[Click Here]({link})", color=0x00ff00)
   await interaction.response.send_message(embed=embed)