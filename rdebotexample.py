import discord
from discord.ext import commands, tasks
import asyncio
import traceback
import sys
from discord import utils
from typing import Union
import random
from datetime import  datetime , timedelta
from discord.utils import  get
import logging
import  json
import os
import string






intents = discord.Intents.default() #IMPORTANT:Enable all Privileged Gateway Intents in https://discord.com/developers/applications/ 
intents.members = True


client = commands.Bot(command_prefix="#Bot prefix here", case_insensitive=True, intent=intents, help_command=None)



@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f'on {len(client.guilds)} servers | r/help')) 
    
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name= 'Red_Dead_Esports  |  r/help'))
    
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name= 'A Song'))
    
    
    print("Logged In...")
    print('#Bot Name If you want')
    print(client.user.id)
    print(client.user.avatar)
    print(client.user.created_at)
    

async def ch_pr():
	await client.wait_until_ready()
	
	statuses = ["Call of Duty Game" , f"on {len(client.guilds)} servers | r/help" , "Red Dead Esports Server" , "JOIN OUR SERVER"]
	
	while not client.is_closed():
		
		status = random.choice(statuses)
		await client.change_presence(activity=discord.Game(name=status))
		
		await asyncio.sleep(10)

client.loop.create_task(ch_pr())


@client.command()
async def hello(ctx):
	await ctx.send(f'Toh Kese H Aap!! {ctx.author.mention}')

@client.command()
async def ping(ctx):
    ping = round(client.latency * 1000)
    await ctx.send(f'🏓Pong `{ping}ms`')









@client.command()
async def bot(ctx):
	
	embed=discord.Embed(title = "**SUPPORT PANEL**" , description= "RED DEAD ESPORTS BOT" , colour= discord.Colour.blue())
	embed.set_footer(text= "MADE BY MISHU aka DSQUADZ GAMING")
	
	embed.add_field(name= "*Servers Using Bot*" , value= f'**{len(client.guilds)}**')
	embed.add_field(name= '*Created On*' , value= client.user.created_at.strftime("%a, %d, %B, %Y, %I:%M %p UTC"))
	
	embed.add_field(name= "Helpful Links" , value= "**INVITE ME**"   "="   "[INVITE](https://discord.com/api/oauth2/authorize?client_id=808734674506743819&permissions=8&scope=bot)" 
	"\n" "**SUPPORT SERVER**" "="  "[JOIN HERE](https://discord.gg/xWMCacJGh5)" "\n" "**GITHUB SUPPORT**" "\n" "`Coming Soon`")
	
	
	await ctx.send(embed=embed)
	

@client.command()
@commands.has_guild_permissions(manage_messages=True)
async def clear(ctx , count: int = None):
	if count is None:
		await ctx.send('**PLEASE ENTER REQUIRED NUMBER TO PURGE**')
	else:
		await ctx.channel.purge(limit=count+1)
		rtmsg = await ctx.send(f"Cleared the last {count} message(s)!!")
		await asyncio.sleep(3)
		await rtmsg.delete()
		

@client.command(name="userinfo", aliases=['ui', 'whois'])
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(
        color=discord.Colour.red(),
        timestamp=ctx.message.created_at,
        description=member.mention
    )

    embed.set_author(name=f"{member} Info")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(
        name="Registered At:",
        value=member.created_at.strftime("%a, %d %b %Y %I:%M %p"),
        inline=False
    )
    embed.add_field(
        name="Joined Server At:",
        value=member.joined_at.strftime("%a, %d %b %Y %I:%M %p"),
        inline=False
    )

    roles = " ".join([role.mention for role in member.roles if role != ctx.guild.default_role])

    if len(roles.strip()) == 0:
        roles = "This user does not have any roles"

    embed.add_field(
        name=f"{len(member.roles)-1} Roles",
        value=roles,
        inline=False
    )
    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)
    

@client.command(name="serverinfo", aliases=['si'])
async def serverinfo(ctx):
    name = ctx.guild.name
    description = ctx.guild.description
    owner = ('||***Hided Due to Security Reason***||')
    guild_id = ctx.guild.id
    region = ctx.guild.region
    member_count = ctx.guild.member_count
    icon = ctx.guild.icon_url

    embed = discord.Embed(
        title=f"{name} Server Information",
        description=description,
        color=discord.Colour.red()
        )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=member_count, inline=True)

    await ctx.send(embed=embed)
	

warn_count = {}

@client.command(name="warn")
@commands.has_guild_permissions(kick_members=True)
async def warn(ctx, user: discord.Member = None, *, reason=None):
    if user is None or reason is None:
        await ctx.send("Insufficient arguments.")
    elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
        await ctx.send("You cannot warn this user because their role is higher than or equal to yours.")
    else:
        print(f"Warning user {user.name} for {reason}...")

        if str(user) not in warn_count:
            warn_count[str(user)] = 1
        else:
            warn_count[str(user)] += 1

        embed = discord.Embed(
            title=f"{user.name} has been warned", color=discord.Colour.red())
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="This user has been warned",
                        value=f"{warn_count[str(user)]} time(s)")

        await ctx.send(content=None, embed=embed)
			

@client.command(name="warncount")
async def warncount(ctx, user: discord.Member):
    if str(user) not in warn_count:
        warn_count[str(user)] = 0

        count = warn_count[str(user)]
        await ctx.send(f"{user.mention} has been warned {count} time(s)")


async def create_mute_role(guild):
    perms = discord.Permissions(send_messages=False)
    mute_role = await guild.create_role(name="Muted", color=discord.Color.dark_grey(), permissions=perms)

    for channel in guild.channels:
        await channel.set_permissions(mute_role, send_messages=False)

    return mute_role



@client.command(name="mute")
@commands.has_guild_permissions(kick_members=True)
async def mute(ctx, user: discord.Member = None, time: str = None):
    if user is None:
        await ctx.send("Insufficient arguments.")
    elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
        await ctx.send("You cannot mute this user because their role is higher than or equal to yours.")
    else:
        guild = ctx.guild
        mute_role = None

        for role in guild.roles:
            if role.name.lower() == "muted":
                mute_role = role
                break

        if mute_role in user.roles:
            await ctx.send("This user is already muted.")
        else:
            if not mute_role:
                await ctx.send("This server does not have a `Muted` Role. Creating one right now.")
                await ctx.send("This may take some time.")
                mute_role = await create_mute_role(guild)

            if time is None:
                await user.add_roles(mute_role)
                await ctx.send(f"User {user.mention} has been muted! They cannot speak.")
            else:
                time_unit = None
                parsed_time = None

                if "s" in time:
                    time_unit = "seconds"
                    parsed_time = time[0:(len(time) - 1)]
                elif "m" in time:
                    time_unit = "minutes"
                    parsed_time = time[0:(len(time) - 1)]
                elif "h" in time:
                    time_unit = "hours"
                    parsed_time = time[0:(len(time) - 1)]
                else:
                    time_unit = "minutes"  # default to minutes if user doesn't provide a time unit
                    parsed_time = time[0:len(time)]

                await user.add_roles(mute_role)
                await ctx.send(f"User {user.mention} has been muted for {parsed_time} {time_unit}! They cannot speak.")

                if time_unit == "seconds":
                    await asyncio.sleep(int(parsed_time))
                elif time_unit == "minutes":
                    await asyncio.sleep(int(parsed_time) * 60)
                elif time_unit == "hours":
                    await asyncio.sleep(int(parsed_time) * 3600)

                await user.remove_roles(mute_role)
                await ctx.send(f"User {user.mention} has been unmuted after {parsed_time} {time_unit}! They can speak now.")


@client.command(name="unmute")
@commands.has_guild_permissions(kick_members=True)
async def unmute(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("Insufficient arguments.")
    elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
        await ctx.send("You cannot unmute this user because their role is higher than or equal to yours.")
    else:
        guild = ctx.guild
        mute_role = None

        for role in guild.roles:
            if role.name.lower() == "muted":
                mute_role = role
                break

        if mute_role in user.roles:
            if not mute_role:
                mute_role = await create_mute_role(guild)

            await user.remove_roles(mute_role)
            await ctx.send(f"User {user.mention} has been unmuted! They can now speak.")

        else:
            await ctx.send("This user was never muted.")


@client.command(name="ban")
@commands.has_guild_permissions(ban_members=True)
async def ban(ctx, user: Union[discord.Member, int], *, reason=None):
    if not isinstance(user, int):
        if ctx.author.top_role.position <= user.top_role.position \
                and ctx.guild.owner_id != ctx.author.id:
            await ctx.send(
                "You cannot ban this user because their role "
                "is higher than or equal to yours."
            )
            return
    if isinstance(user, int):
        user_str = f"<@{user}>"
        user = discord.Object(id=user)
    else:
        user_str = user
    try:
        await user.send(
            f"You have been **banned** from **{ctx.guild}** server "
            f"due to the following reason:\n**{reason}**"
        )
    except Exception:
        pass
    await ctx.guild.ban(user, reason=reason)
    if reason:
        await ctx.send(
            f"User **{user_str}** has been banned for reason: "
            f"**{reason}**."
        )
    else:
        await ctx.send(f"User **{user_str}** has been banned.")


@client.command(name="unban")
@commands.has_guild_permissions(ban_members=True)
@commands.guild_only()
async def unban(
    ctx, user: Union[discord.User, int, str],
    *, reason=None
):
    if isinstance(user, int):
        user_str = f"<@{user}>"
        user = discord.Object(id=user)
    else:
        user_str = user
        
    if isinstance(user, str):
        guild_bans = await ctx.guild.bans()
        try:
            name, tag = user.split('#')
        except:
            await ctx.send(
                "Please format the username like this: "
                "Username#0000"
            )
            return
        banned_user = utils.get(
            guild_bans, user__name=name,
            user__discriminator=tag
        )
        if banned_user is None:
            await ctx.send("I could not find that user in the bans.")
            return
        await ctx.guild.unban(banned_user.user)
        try:
            await banned_user.send(
                f"You have been unbanned with reason: {reason}"
            )
        except Exception:
            pass

    else:
        await ctx.guild.unban(user)
        try:
            await user.send(
                f"You have been unbanned with reason: {reason}"
            )
        except Exception:
            pass

    await ctx.send(f"Unbanned **{user_str}**")


@client.command(name="kick")
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
    if user is None:
        await ctx.send("Insufficient arguments.")
    elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
        await ctx.send("You cannot kick this user because their role is higher than or equal to yours.")
    else:
        await ctx.guild.kick(user, reason=reason)
        if reason:
            await ctx.send(f"User **{user}** has been kicked for reason: **{reason}**.")
        else:
            await ctx.send(f"User **{user}** has been kicked.")
        await user.send(f"You have been **kicked** from **{ctx.guild}** server due to the following reason:\n**{reason}**")


@client.command(name="lockchannel", aliases=['lock'])
@commands.has_guild_permissions(manage_guild=True)
async def lockchannel(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel

    for role in ctx.guild.roles:
        if role.permissions.administrator:
            await channel.set_permissions(role, send_messages=True, read_messages=True)
        elif role.name == "@everyone":
            await channel.set_permissions(role, send_messages=False)

    await ctx.send(f"🔒The channel {channel.mention} has been locked")


@client.command(name="unlockchannel", aliases=['unlock'])
@commands.has_guild_permissions(manage_guild=True)
async def unlockchannel(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel

    await channel.set_permissions(ctx.guild.roles[0], send_messages=True)

    await ctx.send(f"🔓The channel {channel.mention} has been unlocked")


@client.command(name="slowmode", aliases=['sm'])
@commands.has_guild_permissions(manage_guild=True)
async def setdelay(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode in this channel to **{seconds}** seconds!")


@client.command(name="addrole",aliases=['ad'])
@commands.has_permissions(manage_roles = True)
async def addrole(ctx,role: discord.Role ,user: discord.Member):
    await user.add_roles(role)
    await ctx.send(f"Successfully Added {role.mention} to {user.mention}")

@client.command(name= "removerole",aliases=['rd'])
@commands.has_permissions(manage_roles = True)
async def removerole(ctx,role: discord.Role ,user: discord.Member):
    await user.remove_roles(role)
    await ctx.send(f"Successfully Removed {role.mention} to {user.mention}")


@client.command(name="avatar", aliases=['av'])
async def avatar(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    aembed = discord.Embed(
        color=discord.Colour.red(),
        title=f"{user}"
    )

    aembed.set_image(url=f"{user.avatar_url}")
    await ctx.send(embed=aembed)

@client.command()
@commands.has_permissions(administrator=True)
async def say(ctx , *, msg):
    await ctx.message.delete() 
    await ctx.send("{}".format(msg))





@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	
	embed= discord.Embed(
	title = f'Hello {author.name}' , 
	description = "**HERE ARE THE COMMANDS YOU NEED TO KNOW**" ,
	colour = discord.Colour.orange())
	
	embed.add_field(name= "**GENERAL COMMANDS**" , value= "`hello` , `ping` , `help` , `bot`" "\n" "`userinfo` , `serverinfo` , `helpme`")
	embed.add_field(name= "**MODERATOR COMMANDS**" , value= "`kick` , `ban` , `unban` , `mute` , `unmute`" "\n" "`addrole` , `removerole` , `clear` , `warn` , `warncount`")
	embed.add_field(name= "**ADMIN COMMANDS**" , value= "`lockchannel` , `unlockchannel` , `say` , `announce`" "\n" "`poll` , `giveaway`")
	embed.add_field(name= "**FUN COMMANDS**" , value= "`add` , `multiply` , `divide` , `coinflip`" "\n" "`roll` , `dice` , `8ball`")
	
	await ctx.send(f"**Hey! {ctx.author.mention} Please Check Your DM**" , delete_after = 5 )
	await author.send(embed=embed)
	
	







@client.command(pass_context = True)
@commands.has_permissions(manage_channels = True)
async def announce(ctx, channel: discord.TextChannel,*,msg):
    await ctx.send(f'Message sended to {channel}')
    embed = discord.Embed(
    description = msg,
    colour= discord.Colour.red())
    await channel.send(embed=embed)


@client.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@client.group(invoke_without_command=True)
async def helpme(ctx):
	embed = discord.Embed(title= 'Help', description = 'Use r/help <command> to get info')
	
	embed.add_field(name= "Fun" , value= 'add, coinflip , 8ball, roll' '\n' 'multiply , divide , dice')
	
	embed.add_field(name= "Moderation" , value= 'kick , ban , unban , warn' '\n' 'unwarn , mute , unmute')
	await ctx.send(embed=embed)


@helpme.command()
async def kick(ctx):
	embed = discord.Embed(title= "KICK" , 
	description = "Kicks a member from the server" , colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" , value= "*r/kick <member> [reason]*")
	await ctx.send(embed=embed)


@helpme.command()
async def ban(ctx):
	embed = discord.Embed(title= "BAN" , 
	description = "Ban a member from the server" , colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" , value= "*r/ban <member> [reason]*")
	await ctx.send(embed=embed)

@helpme.command()
async def unban(ctx):
	embed = discord.Embed(title= "UNBAN" , 
	description = "Unban a member from the server" , colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" , value= "*r/unban <member> [reason]*")
	await ctx.send(embed=embed)

@helpme.command()
async def mute(ctx):
	embed = discord.Embed(title= "MUTE" , 
	description = "Mute a member from the server" , colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" , value= "*r/mute <member> [reason]*")
	await ctx.send(embed=embed)

@helpme.command()
async def unmute(ctx):
	embed = discord.Embed(title= "UNMUTE" , 
	description = "unmute a member from the server" , colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" , value= "*r/unmute <member> [reason]*")
	await ctx.send(embed=embed)


@helpme.command()
async def warn(ctx):
	embed = discord.Embed(title= "WARN" , 
	description = "warns a member of the server" , colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" , value= "*r/warn <member> [reason]*")
	await ctx.send(embed=embed)

@helpme.command()
async def add(ctx):
	embed = discord.Embed(title= "ADD" , 
	description = "Can add two numbers" , 
	colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" ,value= "*r/add <num-1> <num-2>*")
	await ctx.send(embed=embed)

@helpme.command()
async def _8ball(ctx):
	embed = discord.Embed(title= "8 Ball" , 
	description = "Randomly Select Yes or No" , 
	colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" ,value= "*r/8ball <Your Question*")
	await ctx.send(embed=embed)

@helpme.command()
async def coinflip(ctx):
	embed = discord.Embed(title= "COINFLIP" , 
	description = "Gives Heads or Tails" , 
	colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" ,value= "*r/cf or r/coinflip*")
	await ctx.send(embed=embed)

@helpme.command()
async def roll(ctx):
	embed = discord.Embed(title= "ROLL" , 
	description = "Rolls a number b/w 1-100" , 
	colour = discord.Colour.teal())
	
	embed.add_field(name= "**SYNTAX**" ,value= "*r/roll*")
	await ctx.send(embed=embed)


@client.command(aliases=['8ball'])
async def _8ball(ctx, *,question):
    responses = ['Definitely',
                 'Umm , Maybe!!', 'Probably Yes', 'Not at all', 'This is definitely gonna happen!', 'I prefer Nope', 'I cannot decide', 'Are u satisfied with your question ?']
    await ctx.send(f'Question: {question}\nAnswer : {random.choice(responses)}')



@client.command()
async def roll(ctx):
	n= random.randrange(1 , 101)
	await ctx.send(n)

@client.command()
async def dice(ctx):
	d= random.randrange(1, 6)
	await ctx.send(d)



@client.command()
async def multiply(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left * right)


@client.command()
async def divide(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left / right)











@client.command(name = 'giveaway' , aliases = ['gstart'])
@commands.has_permissions(manage_guild = True)
async def giveaway(ctx):
    await ctx.send(embed=discord.Embed(color=discord.Color.green(), title = "Select the channel, you would like the giveaway to be in"))
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg1 = await client.wait_for('message', check = check, timeout=30.0)

        channel_converter = discord.ext.commands.TextChannelConverter()
        try:
            giveawaychannel = await channel_converter.convert(ctx, msg1.content)
        except commands.BadArgument:
            return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title = "This channel doesn't exist, please try again"))

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again!")
    if not giveawaychannel.permissions_for(ctx.guild.me).send_messages or  not giveawaychannel.permissions_for(ctx.guild.me).add_reactions:
        return await ctx.send(embed=discord.Embed(color=discord.Color.red(), description = f"Bot does not have correct permissions to send in: {giveawaychannel}\n **Permissions needed:** ``Add reactions | Send messages``"))

    await ctx.send(embed=discord.Embed(color=discord.Color.green(), title = "How many winners to the giveaway would you like?"))
    try:
        msg2 = await client.wait_for('message', check = check, timeout=30.0)
        try:
            winerscount = int(msg2.content)
        except ValueError:
            return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title = "You didn't specify a number of winners, please try again."))

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again!")

    await ctx.send(embed=discord.Embed(color=discord.Color.green(), title = "Select an amount of time for the giveaway."))
    try:
        since = await client.wait_for('message', check = check, timeout=30.0)

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again!")


    seconds = ("s", "sec", "secs", 'second', "seconds")
    minutes= ("m", "min", "mins", "minute", "minutes")
    hours= ("h", "hour", "hours")
    days = ("d", "day", "days")
    rawsince = since.content
    try:
        time = int(since.content.split(" ")[0])
    except ValueError:
        return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title = "You did not specify a unit of time, please try again."))
    since = since.content.split(" ")[1]
    if since.lower() in seconds:
        timewait = time
    elif since.lower() in minutes:
        timewait = time*60
    elif since.lower() in hours:
        timewait = time*3600
    elif since.lower() in days:
        timewait = time*86400
    elif since.lower() in weeks:
        timewait = time*604800
    else:
        return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title = "You did not specify a unit of time, please try again."))
        
    prizeembed = discord.Embed(title = "What would you like the prize to be?" , color = discord.Color.green())
    await ctx.send(embed = prizeembed)
    try:
        msg4 = await client.wait_for('message', check = check, timeout=30.0)


    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again.")

    logembed = discord.Embed(title = "Giveaway Logged" , description = f"**Prize:** ``{msg4.content}``\n**Winners:** ``{winerscount}``\n**Channel:** {giveawaychannel.mention}\n**Host:** {ctx.author.mention}" , color = discord.Color.red())
    logembed.set_thumbnail(url = ctx.author.avatar_url)
    
    guild = client.get_guild(808630460846440489) # Put your guild ID here!
    logchannel = guild.get_channel(809710676872003595) # Put your channel, you would like to send giveaway logs to.
    await logchannel.send(embed = logembed)

    futuredate = datetime.utcnow() + timedelta(seconds=timewait)
    embed1 = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title=f"🎉GIVEAWAY🎉\n`{msg4.content}`",timestamp = futuredate, description=f'React with 🎉 to enter!\nEnd Date: {futuredate.strftime("%a, %b %d, %Y %I:%M %p")}\nHosted by: {ctx.author.mention}')
    
    embed1.set_footer(text=f"Giveaway will end")
    msg = await giveawaychannel.send(embed=embed1)
    await msg.add_reaction("🎉")
    await asyncio.sleep(timewait)
    message = await giveawaychannel.fetch_message(msg.id)
    for reaction in message.reactions:
        if str(reaction.emoji) == "🎉":
            users = await reaction.users().flatten()
            if len(users) == 1:
                return await msg.edit(embed=discord.Embed(title="Nobody has won"))

    winners = random.sample([user for user in users if not user.bot], k=winerscount)
    
    #await message.clear_reactions()
    winnerstosend = "\n".join([winner.mention for winner in winners])

    win = await msg.edit(embed = discord.Embed(title = "WINNER" , description = f"Congratulations {winnerstosend}, you have won **{msg4.content}**!" , color = discord.Color.blue()))


@client.command()
@commands.has_permissions(manage_guild = True)
async def reroll(ctx):
    async for message in ctx.channel.history(limit=100 , oldest_first = False):
        if message.author.id == client.user.id and message.embeds:
            reroll = await ctx.fetch_message(message.id)
            users = await reroll.reactions[0].users().flatten()
            users.pop(users.index(client.user))
            winner = random.choice(users)
            await ctx.send(f"The new winner is {winner.mention}")
            break
    else:
        await ctx.send("No giveaways going on in this channel.")


@client.command(name= "coinflip" , aliases= ['cf'])
async def coinflip(ctx):
	choices = ["Heads" , "Tails"]
	rancoin = random.choice(choices)
	await ctx.send(rancoin)


@client.command(name= "youtube" , aliases= ['yt'])
async def youtube(ctx):
	embed = discord.Embed(
	title= '**MY YOUTUBE LINK**' , description= '[CLICK HERE TO GO](#Put your Youtube link here)' , colour = discord.Colour.dark_gold())
	await ctx.send(embed=embed)
	








@client.event
async def on_command_error(ctx, error):
    try:
        error = error.original
    except Exception:
        pass
    if type(error) is discord.ext.commands.errors.CommandNotFound:
        return
    elif type(error) is discord.ext.commands.errors.BadArgument:
        pass
    elif type(error) is discord.ext.commands.errors.MissingRequiredArgument:
        pass
    elif type(error) is discord.ext.commands.errors.NoPrivateMessage:
        pass
    elif type(error) is discord.ext.commands.errors.MissingPermissions:
        pass
    elif type(error) is discord.ext.commands.errors.NotOwner:
        pass
    elif type(error) is discord.ext.commands.errors.CommandOnCooldown:
        pass
    elif type(error) is discord.ext.commands.errors.ChannelNotFound:
        pass
    elif type(error) is discord.ext.commands.errors.BadUnionArgument:
        pass
    elif type(error) is discord.ext.commands.errors.BotMissingPermissions:
        pass
    elif type(error) is discord.errors.Forbidden:
        error = "I don't have permission to do that!"
    else:
        print(f"Error {type(error)}: {error}")
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

        embed = discord.Embed(
            title='Error!',
            description='An unexpected error ocurred.\
                Please report this to the dev.',
        )
        embed.add_field(
            name='Error Message:',
            value=f"{type(error)}:\n{error}",
            inline=False
        )
    await ctx.send(f"{error}")

client.run('#Put Your bot token here')
