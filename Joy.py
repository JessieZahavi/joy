#!/usr/bin/env python3

import os
import time
import random
import asyncio
import logging
from tkinter import Image


import json
import re

import discord

import twitchlive
import self as self
from discord import Object
from discord.ext import commands
from discord.utils import get
from discord import Member, Emoji
import sys
import configparser
import requests

# id = 485108935771029516
from discord.ext.commands import bot


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = 'j!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command()
async def new(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    embed = discord.Embed(
        title=f'The new prefix is: {prefix}', color=0xf8a1a1)
    await ctx.channel.send(content=None, embed=embed)


@client.command()
async def subrole(ctx):
    embed = discord.Embed(
        title="TWITCH SUBSCRIBER ROLE\n\n"
              "To receieve the Subscribers Role please link your twitch account to discord (Settings > Connections > "
              "Twitch Icon) and wait thirty minutes to an hour.", color=0xf8a1a1)
    if not lock_handler():
        return
    await ctx.channel.send(
        content=None, embed=embed)


@client.command()
async def info(ctx):
    embed = discord.Embed(title="Helloo I'm Joy! Pleased to help you!",
                          description="Use j! as a prefix before every command", color=0xf8a1a1)
    embed.add_field(name="new", value="To set new prefix", inline=False)
    embed.add_field(name="subrole", value="Instructions to link discord to twitch!", inline=False)
    embed.add_field(name="fc", value="To know about friendcodes", inline=False)
    embed.add_field(name="sw", value="To know about switchcodes", inline=False)
    embed.add_field(name="league", value="To know about the league")
    if not lock_handler():
        return
    await ctx.channel.send(
        content=None, embed=embed)


@client.event
async def on_message(m=None, emoji: Emoji = None):
    regex_code = r'([Hh]{1,7})([Ii]{1,7})((!){1,15})?(((:){1,15})([A-Za-z]{1,10})((:){1,15}))?((<){1,15})?((3){1,15})?((\s){0,})'
    regex_code1 = r'(([Hh]{1,10})([Ee]{1,10})([Ll]{1,10})([Oo]{1,10}))((!){1,15})?(((:){1,15})([A-Za-z]{1,10})((:){1,15}))?((<){1,15})?((3){1,15})?'
    regex_code2 = r'((([Nn]{1,10})([Ii]{1,10})([Tt]{1,10})([Ee]{1,10})))((!){1,15})?(((:){1,15})([A-Za-z]{1,10})((:){1,15}))?((<){1,15})?((3){1,15})?'
    regex_code3 = r'((([Gg]{1,10})([Oo]{1,10})([Dd]{1,10})([Nn]{1,10})([Ii]{1,10})([Gg]{1,10})([Hh]{1,10})([Tt]{1,10})))((!){1,15})?(((:){1,15})([A-Za-z]{1,10})((:){1,15}))?((<){1,15})?((3){1,15})?'
    regex_code4 = r'[Ff]{1}'
    regex_code5 = r'(([Mm]{1,10})([Oo]{1,10})([Rr]{1,10})([Nn]{1,10})([Ii]{1,10})([Nn]{1,10})([Gg]{1,10}))((!){1,15})?(((:){1,15})([A-Za-z]{1,10})((:){1,15}))?((<){1,15})?((3){1,15})?'
    regex_code6 = r'([Gg]{1,7})([Oo]{1,14})([Dd]{1,7})((\s){1,2})?([Mm]{1,7})([Oo]{1,7})([Rr]{1,7})([Nn]{1,7})([Ii]{1,7})([Nn]{1,7})([Gg]{1,7})((!){1,15})?(((:){1,15})([A-Za-z]{1,10})((:){1,15}))?((<){1,15})?((3){1,15})?'
    regex_code7 = r'([Rr]{1,7})([Ii]{1,7})([Pp]{1,7})((!){1,15})?'

    if m.content is not None:
        if re.fullmatch(regex_code, m.content):
            await greeting_handler(m)
        if re.match(regex_code1, m.content):
            await greeting_handler(m)
        if re.match(regex_code2, m.content):
            await nite_handler(m)
        if re.match(regex_code3, m.content):
            await nite_handler(m)
        if re.fullmatch(regex_code4, m.content):
            await f_handler(m)
        if re.fullmatch(regex_code7, m.content):
            await f_handler(m)
        if re.match(regex_code5, m.content):
            await morning_handler(m)
        if re.match(regex_code6, m.content):
            await morning_handler(m)
        if m.content == "Clown":
            await clown_handler(m)
        if m.content.startswith("^"):
            await arrow_handler(m)
        if m.content.startswith("Pachi"):
            await pachi_handler(m)
        if m.content.startswith("pachi"):
            await pachi_handler(m)
    elif emoji is not None:
        print("lol")
        if emoji.name == "spider81Stormdab":
            await dab_handler(emoji)

    await client.process_commands(m)


async def dab_handler(m):
    await m.channel.send(client.get_emoji(651264646208159755))


async def error_fc_handler(m):
    embed = discord.Embed(
        title=" Wrong format! :x: The code must be a series of numbers using the next format: XXXX-XXXX-XXXX :heart: ",
        color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def error_sw_handler(m):
    embed = discord.Embed(
        title=" Whoopsiees! Wrong format! :x: Try inputting your code using the next format: SW-XXXX-XXXX-XXXX :heart:",
        color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def error_paste_handler(m):
    embed = discord.Embed(
        title=" Whoopsiees! Wrong link! :x: The url must be a valid pokepast link :heart: ", color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def reg_handler(m):
    embed = discord.Embed(
        title="Code has been registered :heart:", color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def f_handler(m):
    if not lock_handler():
        return
    await m.channel.send(client.get_emoji(638476125869441034))


async def update_handler(m):
    embed = discord.Embed(
        title="Code has been updated :heart:", color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def delete_handler(m):
    embed = discord.Embed(
        title="Code has been delete :heart:", color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def already_handler(m):
    embed = discord.Embed(
        title="Code already registered :heart:", color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def user_handler(m):
    embed = discord.Embed(
        title="Code is already registered by a different user :heart:", color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def errorFc_handler(m):
    embed = discord.Embed(
        title="Wrong format! It should be XXXX-XXXX-XXXX :heart:", color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def code_handler(m):
    embed = discord.Embed(
        title="Your friend code is: " + fc[str(m.message.author.id)] + " :heart:", color=0xf8a1a1)
    await m.channel.send(content=None, embed=embed)


async def no_code_handler(m):
    embed = discord.Embed(
        title="You don't have a code registered :heart:", color=0xf8a1a1)
    await m.channel.send(content=None, embed=embed)


async def del_code_handler(m):
    embed = discord.Embed(
        title="Code deleted :heart:", color=0xf8a1a1)
    await m.channel.send(content=None, embed=embed)


async def no_user_handler(m):
    embed = discord.Embed(
        title="This user doesn't have a code registered :heart:", color=0xf8a1a1)
    await m.channel.send(content=None, embed=embed)


async def no_team_handler(m):
    embed = discord.Embed(
        title="This user doesn't have a team registered :heart:", color=0xf8a1a1)
    await m.channel.send(content=None, embed=embed)


async def greeting_handler(m):
    if not lock_handler():
        return
    await m.channel.send(m.author.mention + " Hii sweetiee!! :heart:")


async def nite_handler(m):
    if not lock_handler():
        return
    await m.channel.send(m.author.mention + " Sweet dreams sweetiee!! :heart:")


async def morning_handler(m):
    if not lock_handler():
        return
    await m.channel.send(m.author.mention + " Rise and Shine pumpkin!! :coffee:")


async def arrow_handler(m):
    if not lock_handler():
        return
    await m.channel.send("^")


async def clown_handler(m):
    if not lock_handler():
        return
    await m.channel.send(" Pachi is a :clown: https://bit.ly/2OArVGa")


async def pachi_handler(m):
    await m.channel.send(":clown:")


def lock_handler():
    lockFile = "/temp/.joylock"
    if os.path.isfile(lockFile):
        fileTime = os.path.getmtime(lockFile)
        if time.time() - fileTime >= 20:
            os.remove(lockFile)
            f = open(lockFile, 'w+')
            f.close()
            return True
        return False
    f = open(lockFile, 'w+')
    f.close()
    return True


@client.event
async def on_member_update(before, after):
    await live_handler(after)
    await live_poke(after)
    await go_live_handler(after)


async def sync_handler(m):
    userCount = 0
    for user in m.guild.members:
        userCount += 1
        await live_handler(user)
        await go_live_handler(user)
    logging.info("sync_handler,synced {} users".format(userCount))


async def live_handler(after):
    live_role = after.guild.get_role(647448861916266526)
    live_role_exists = False
    for role in after.roles:
        if role == live_role:
            live_role_exists = True
            break
    live_streaming = False
    for act in after.activities:
        if act.type == discord.ActivityType.streaming:
            live_streaming = True
            break
    if not live_streaming:
        if live_role_exists:
            await after.remove_roles(live_role, )
            logging.info("live_handler,removing role from {}, not streaming"
                         .format(after.name))
        return
    sub_role = False
    for role in after.roles:
        if role.id == 619600861034708992:
            sub_role = True
    if not sub_role:
        return
    if live_role_exists:
        return
    if live_streaming:
        await after.add_roles(live_role, )
        logging.info("live_handler,adding role to {}".format(after.name))
        return


async def live_poke(after):
    live_now = after.guild.get_role(650565137039884308)
    live_role_exists = False
    for role in after.roles:
        if role == live_now:
            live_role_exists = True
            break
    live_streaming = False
    for act in after.activities:
        if act.type == discord.ActivityType.streaming:
            live_streaming = True
            break
    if not live_streaming:
        if live_role_exists:
            await after.remove_roles(live_now, )
            logging.info("live_handler,removing role from {}, not streaming"
                         .format(after.name))
        return

    sub_role = False
    for role in after.roles:
        if role.id == 603364112713646099:
            sub_role = True
    if not sub_role:
        return
    if live_role_exists:
        return
    if live_streaming:
        await after.add_roles(live_now, )
        logging.info("live_handler,adding role to {}".format(after.name))
        return


async def go_live_handler(after):
    channel = client.get_channel(651097688447778817)
    going_live = after.guild.get_role(630876670236033026)
    going_live_exists = False
    for role in after.roles:
        if role == going_live:
            going_live_exists = True
            break
    live_streaming = False
    for act in after.activities:
        if act.type == discord.ActivityType.streaming:
            live_streaming = True
            break
    if live_streaming:
        if going_live_exists:
            return


friendcodes = {}
switchcodes = {}
fortrade = {}
lookingfor = {}
pokepast = {}
tiffemo = {}
emotedict = {}
announcement = {}


@client.event
async def on_ready():
    global friendcodes, lookingfor, fortrade
    global switchcodes, pokepast, tiffemo, announcement

    try:
        with open('switchcodes.json') as f:
            switchcodes = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        switchcodes = {}

    try:
        with open('friendcodes.json') as f:
            friendcodes = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        friendcodes = {}

    try:
        with open('lookingfor.json') as f:
            lookingfor = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        lookingfor = {}

    try:
        with open('fortrade.json') as f:
            fortrade = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        fortrade = {}

    try:
        with open('pokepast.json') as f:
            pokepast = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        pokepast = {}

    try:
        with open('tiffemo.json') as f:
            tiffemo = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        tiffemo = {}

    try:
        with open('pokepast.json') as f:
            pokepast = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        pokepast = {}

    try:
        with open('emotedict.json') as f:
            emotedict = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        emotedict = {}

    try:
        with open('announcement.json') as f:
            announcement = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        announcement = {}


async def fcs(ctx, member: Member):
    regex_code = r'.*[#][0-9]{4}'
    if re.match(regex_code, str(member)):
        if str(member.id) in friendcodes:
            embed = discord.Embed(
                title=str(member.display_name) + "'s code is: " + friendcodes[str(member.id)] + " :heart:",
                color=0xf8a1a1)
            return await ctx.channel.send(content=None, embed=embed)

        else:
            return await no_user_handler(ctx)
    else:
        return await errorFc_handler(ctx)


async def sws(ctx, member: Member):
    regex_code = r'.*[#][0-9]{4}'

    if re.match(regex_code, str(member)):
        if str(member.id) in switchcodes:
            embed = discord.Embed(
                title=str(member.display_name) + "'s code is: " + switchcodes[str(member.id)] + " :heart:",
                color=0xf8a1a1)
            return await ctx.channel.send(content=None, embed=embed)
        else:
            return await no_user_handler(ctx)
    else:
        return await errorFc_handler(ctx)


async def past(ctx, member: Member):
    regex_code = r'.*[#][0-9]{4}'
    if re.match(regex_code, str(member)):
        if str(member.id) in pokepast:
            embed = discord.Embed(
                title=str(member.display_name) + "'s team is: " + pokepast[str(member.id)] + ":heart:", color=0xf8a1a1)
            return await ctx.channel.send(content=None, embed=embed)
        else:
            return await no_team_handler(ctx)
    else:
        return await errorFc_handler(ctx)


@client.command()
async def rules(m):
    embed = discord.Embed(
        title="Rules",
        description="1. Discrimination of any kind (gender, sexuality, race) is _***NOT***_ allowed.\n\n"
                    "2. Any real life pictures that are lewd aren't allowed whatsoever. This also includes links, videos and audio.\n\n"
                    "3. You are allowed to poke fun at someone, but only if they're okay with it. If they ask you to stop, you must stop.\n\n"
                    "4. No engaging in sexual jokes.\n\n"
                    "5. Drama must be taken outside the server. Furthermore, all discussion on said drama must stop as well.\n 5a. Discussions of bans or people who are muted are also not allowed.\n\n"
                    "6. Self advertising is not allowed. You may only self advertise in `#partnership-advertising`.\n6b. Discord channels are not allowed to be advertised whatsoever.\n\n"
                    "7. Please keep discussion to their relevant channels.\n\n"
                    "8. No spamming of any form, unless the channel is meant for posting pictures of certain content.\n However, only content of the channel's nature is allowed.\n\n"
                    "9. Discussing politics of any kind is not allowed.\n\n"
                    "10. Impersonation of anybody is not allowed. This includes changing your name/pfp to match someone else's.\n\n"
                    "11. Private Message invites are not allowed. If someone got an invite to join some other server by DM , don’t hesitate and tell the _`@Tops`_ to take care of it.\n\n"
                    "12. For any problem please DM the `@Tops` to solve it.\n\n",
        color=0xf8a1a1)

    return await m.channel.send(content=None, embed=embed)


@client.command()
@commands.has_role(619601471838617612)
async def Trules(m):
    embed = discord.Embed(
        title="Rules",
        description="1. Discrimination of any kind (gender, sexuality, race) is _***NOT***_ allowed.\n\n"
                    "2. Any real life pictures that are lewd aren't allowed whatsoever. This also includes links, videos and audio.\n\n"
                    "3. You are allowed to poke fun at someone, but only if they're okay with it. If they ask you to stop, you must stop.\n\n"
                    "4. No engaging in sexual jokes.\n\n"
                    "5. Drama must be taken outside the server. Furthermore, all discussion on said drama must stop as well.\n 5a. Discussions of bans or people who are muted are also not allowed.\n\n"
                    "6. Self advertising is not allowed. You may only self advertise in `#live-streams-stuff`.\n6b. Discord channels are not allowed to be advertised whatsoever.\n\n"
                    "7. Please keep discussion to their relevant channels.\n\n"
                    "8. No spamming of any form, unless the channel is meant for posting pictures of certain content.\n However, only content of the channel's nature is allowed.\n\n"
                    "9. Discussing politics of any kind is not allowed.\n\n"
                    "10. Impersonation of anybody is not allowed. This includes changing your name/pfp to match someone else's.\n\n"
                    "11. Private Message invites are not allowed. If someone got an invite to join some other server by DM , don’t hesitate and tell the _`@ADMIN`_ to take care of it.\n\n"
                    "12. For any problem please DM the `@ADMIN` to solve it.\n\n",
        color=0xf8a1a1)

    return await m.channel.send(content=None, embed=embed)


@client.command()
@commands.has_role(619601471838617612)
async def Tschedule(m):
    embed = discord.Embed(
        title="__**SCHEDULE**__\n\n",
        description="**-Sunday:** TBD\n"
                    "**-Monday:** OFF\n"
                    "**-Tuesday:** 8:30pm EST\n"
                    "**-Wednesday:** OFF\n"
                    "**-Thursday:** 8:30pm EST\n"
                    "**-Friday:** TBD\n"
                    "**-Saturday:** 7:30pm EST\n\n\n"
                    "Tiff will probably be on during the TBD days - but who knows when. It’ll be a little mystery you can solve. \n\n",
        color=0xf8a1a1)

    return await m.channel.send(content=None, embed=embed)


@client.command()
@commands.has_role(619601471838617612)
async def Tsocial(m):
    embed = discord.Embed(
        title="SOCIAL",
        description="TWITCH: https://twitch.tv/SpiderTiff\n\n"
                    "TWITTER: https://twitter.com/spidertiff\n\n"
                    "INSTAGRAM: https://www.instagram.com/spideytiff",
        color=0xf8a1a1)
    return await m.channel.send(content=None, embed=embed)


async def info_fc(m):
    embed = discord.Embed(
        title="The inputs for this command are:", color=0xf8a1a1)
    embed.add_field(name="get",
                    value="To get a battler's code type the command followed by the keyword **get** and tag the user. Example: j!fc get @username#0000",
                    inline=False)
    embed.add_field(name="del",
                    value="To delete your code type the command followed by the keyword **del**. Example: j!fc del",
                    inline=False)
    embed.add_field(name="myfc",
                    value="To get your code type the command followed by the keyword **myfc**. Example: j!fc myfc",
                    inline=False)
    embed.add_field(name="info",
                    value="To know what the command does type the command followed by the keyword **info** Example: j!fc info")
    return await m.channel.send(content=None, embed=embed)


async def info_sw(m):
    embed = discord.Embed(
        title="The inputs for this command are:", color=0xf8a1a1)
    embed.add_field(name="get",
                    value="To get a battler's code type the command followed the keyword **get** and tag the user. Example: j!sw get @username#0000",
                    inline=False)
    embed.add_field(name="del",
                    value="To delete your code type the command followed by the keyword **del**. Example: j!sw del",
                    inline=False)
    embed.add_field(name="mysw",
                    value="To get your code type the command followed by the keyword **myfc**. Example: j!sw mysw",
                    inline=False)
    embed.add_field(name="info",
                    value="To know what the command does type the command followed by the keyword **info** Example: j!sw info")
    return await m.channel.send(content=None, embed=embed)


async def info_paste(m):
    embed = discord.Embed(
        title="The inputs for this command are:", color=0xf8a1a1)
    embed.add_field(name="get",
                    value="To get a challenger's team type the command followed the keyword **get** and tag the user. Example: j!league get @username#0000\n",
                    inline=False)
    embed.add_field(name="del",
                    value="To delete a challenger's team type the command followed by the keyword **del**. Example: j!league del\n",
                    inline=False)
    embed.add_field(name="myteam",
                    value="To get your team type the command followed by the keyword **myteam**. Example: j!league team\n",
                    inline=False)
    embed.add_field(name="info",
                    value="To know what the command does type the command followed by the keyword **info** Example: j!team info")
    return await m.channel.send(content=None, embed=embed)


async def input_handler(m):
    embed = discord.Embed(
        title="The inputs for this command are:", color=0xf8a1a1)
    embed.add_field(name="Keywords:",
                    value="info, myfc, get and del. For more information type the command with or without the keyword info :heart:")
    return await m.channel.send(content=None, embed=embed)


@client.command()
# @commands.has_role()@commands.has_any_role('Library Devs', 'Moderators', 492212595072434186) role permissions to use command
# @commands.has_any_role(619601471838617612,650446167263674398,536057136065544223,550150779261157386,645652785135747077)
async def fc(ctx, code=None, member: Member = None):
    regex_code = r'(^(([0-9]{4})+[-]{1}){2})+([0-9]{4})'
    regex_code1 = r'.*[#][0-9]{4}'
    with open('friendcodes.json', 'r') as f:
        friendcodes = json.load(f)

    if code is not None or member is not None:
        if code != "get":
            if re.match(regex_code, code):
                if (str(ctx.message.author.id)) not in friendcodes:
                    if len(friendcodes) > 0:
                        for i in friendcodes.items():
                            if code in str(i):
                                await user_handler(ctx)
                                break

                            elif code not in str(i):
                                friendcodes[str(ctx.message.author.id)] = code
                                with open('friendcodes.json', 'w') as f:
                                    json.dump(friendcodes, f, indent=4)
                                await reg_handler(ctx)
                                break

                    else:
                        friendcodes[str(ctx.message.author.id)] = code
                        with open('friendcodes.json', 'w') as f:
                            json.dump(friendcodes, f, indent=4)
                        await reg_handler(ctx)

                elif code == friendcodes[str(ctx.message.author.id)]:
                    await already_handler(ctx)

                else:
                    if (str(ctx.message.author.id)) in friendcodes:
                        for i in friendcodes.items():
                            if code in str(i):
                                await user_handler(ctx)
                                break
                            if code not in str(i):
                                friendcodes[str(ctx.message.author.id)] = code
                                with open('friendcodes.json', 'w') as f:
                                    json.dump(friendcodes, f, indent=4)
                                await update_handler(ctx)
                                break
            elif code == "myfc":
                if str(ctx.message.author.id) in friendcodes:
                    embed = discord.Embed(
                        title="Your friend code is: " + friendcodes[str(ctx.message.author.id)] + " :heart:",
                        color=0xf8a1a1)
                    await ctx.channel.send(content=None, embed=embed)
                else:
                    await no_code_handler(ctx)

            elif code == "del":
                if str(ctx.message.author.id) in friendcodes:
                    friendcodes.pop(str(ctx.message.author.id))
                    with open('friendcodes.json', 'w') as f:
                        json.dump(friendcodes, f, indent=4)
                    await del_code_handler(ctx)
                else:
                    await no_code_handler(ctx)

            elif code == "info":
                await info_fc(ctx)

            elif re.match(regex_code1, code):

                await ctx.channel.send(friendcodes[str(member.id)])
            else:
                await error_fc_handler(ctx)

        elif member is not None:
            await fcs(ctx, member)

        else:
            await info_fc()
    else:
        await info_fc(ctx)


@client.command()
# @commands.has_any_role(646036837059526666,550150779261157386,536057136065544223)
async def league(ctx, code=None, member: Member = None):
    regex_code = r'(https:[/]{2})?(pokepast.es[/]{1})[a0-z9]{15,19}'
    regex_code1 = r'.*[#][0-9]{4}'
    with open('pokepast.json', 'r') as f:
        pokepast = json.load(f)

    if code is not None or member is not None:
        if code != "get":
            if re.match(regex_code, code):
                if (str(ctx.message.author.id)) not in pokepast:
                    if len(pokepast) > 0:
                        for i in pokepast.items():
                            if code in str(i):
                                await user_handler(ctx)
                                break

                            elif code in str(i):
                                pokepast[str(ctx.message.author.id)] = code
                                with open('pokepast.json', 'w') as f:
                                    json.dump(pokepast, f, indent=4)
                                await reg_handler(ctx)
                                break

                elif code == pokepast[str(ctx.message.author.id)]:
                    await already_handler(ctx)

                else:
                    if (str(ctx.message.author.id)) in pokepast:
                        for i in pokepast.items():
                            if code in str(i):
                                await user_handler(ctx)
                                break
                            if code not in str(i):
                                pokepast[str(ctx.message.author.id)] = code
                                with open('pokepast.json', 'w') as f:
                                    json.dump(pokepast, f, indent=4)
                                await update_handler(ctx)
                                break
            elif code == "myteam":
                if str(ctx.message.author.id) in pokepast:
                    embed = discord.Embed(
                        title="Your friend code is: " + pokepast[str(ctx.message.author.id)] + " :heart:",
                        color=0xf8a1a1)
                    await ctx.channel.send(content=None, embed=embed)
                else:
                    await no_code_handler(ctx)

            elif code == "del":
                if str(ctx.message.author.id) in pokepast:
                    pokepast.pop(str(ctx.message.author.id))
                    with open('pokepast.json', 'w') as f:
                        json.dump(pokepast, f, indent=4)
                    await del_code_handler(ctx)
                else:
                    await no_code_handler(ctx)
            elif code == "info":
                await info_paste(ctx)

            elif re.match(regex_code1, code):

                await ctx.channel.send(friendcodes[str(member.id)])
            else:
                await error_paste_handler(ctx)

        elif member is not None:
            await fcs(ctx, member)

        else:
            await info_paste()
    else:
        await info_paste(ctx)


@client.command()
# @commands.has_any_role(619601471838617612,650446167263674398,536057136065544223,550150779261157386,645652785135747077)
async def sw(ctx, code=None, member: Member = None):
    regex_code = r'([S][W][-]{1}(([0-9]{4})+[-]{1}){2})+([0-9]{4})'
    regex_code1 = r'.*[#][0-9]{4}'
    with open('switchcodes.json', 'r') as f:
        switchcodes = json.load(f)

    if code is not None or member is not None:
        if code != "get":
            if re.match(regex_code, code):
                if (str(ctx.message.author.id)) not in switchcodes:
                    if len(switchcodes) > 0:
                        for i in switchcodes.items():
                            if code in str(i):
                                await user_handler(ctx)
                                break

                            elif code not in str(i):
                                switchcodes[str(ctx.message.author.id)] = code
                                with open('switchcodes.json', 'w') as f:
                                    json.dump(switchcodes, f, indent=4)
                                await reg_handler(ctx)
                                break

                elif code == switchcodes[str(ctx.message.author.id)]:
                    await already_handler(ctx)

                else:
                    if (str(ctx.message.author.id)) in switchcodes:
                        for i in switchcodes.items():
                            if code in str(i):
                                await user_handler(ctx)
                                break
                            if code not in str(i):
                                switchcodes[str(ctx.message.author.id)] = code
                                with open('switchcodes.json', 'w') as f:
                                    json.dump(switchcodes, f, indent=4)
                                await update_handler(ctx)
                                break
            elif code == "mysw":
                if str(ctx.message.author.id) in switchcodes:
                    embed = discord.Embed(
                        title="Your switch code is: " + switchcodes[str(ctx.message.author.id)] + " :heart:",
                        color=0xf8a1a1)
                    await ctx.channel.send(content=None, embed=embed)
                else:
                    await no_code_handler(ctx)

            elif code == "del":
                if str(ctx.message.author.id) in switchcodes:
                    switchcodes.pop(str(ctx.message.author.id))
                    with open('switchcodes.json', 'w') as f:
                        json.dump(switchcodes, f, indent=4)
                    await del_code_handler(ctx)
                else:
                    await no_code_handler(ctx)

            elif code == "info":
                await info_sw(ctx)

            elif re.match(regex_code1, code):

                await ctx.channel.send(switchcodes[str(member.id)])
            else:
                await error_sw_handler(ctx)

        elif member is not None:
            await sws(ctx, member)

        else:
            await info_sw(ctx)
    else:
        await info_sw(ctx)


emoji = discord.Emoji


@client.command(pass_context=True)
async def respond(ctx, emoji: Emoji):
    with open('tiffemo.json', 'r') as f:
        tiffemos = json.load(f)

    tiffemo[str(emoji.id)] = emoji.name

    with open('tiffemo.json', 'w') as f:
        json.dump(tiffemo, f, indent=4)


@client.command()
async def rip(ctx):
    await ctx.channel.send(client.get_emoji(485100569778978819))


@client.command()
@commands.has_role(619601471838617612)
async def em(ctx, emoji: Emoji):
    with open('emotedict.json', 'r') as f:
        emotedict = json.load(f)

    tiffemo[str(emoji.id)] = emoji.name

    with open('emotedict.json', 'w') as f:
        json.dump(tiffemo, f, indent=4)


@client.command()
# @commands.has_role(619601471838617612)
async def ann(ctx, *message):
    regex_code = r'((\*){2}[A-Za-z]\w+)'
    regex_code1 = r'[A-Za-z]\w+'
    regex_code2 = r'[A-Za-z]\w+([\:])?(\*){2}'
    regex_code3 = r'((\*){2}[A-Za-z]\w+)([\:])?(\*){2}'
    temp = []
    description = []
    y = 0

    try:
        if message is not ():
            if re.match(regex_code3, message[0]):
                title = message[0]
            elif re.match(regex_code, message[0]):
                for x in range(1, len(message)):
                    if re.fullmatch(regex_code1, message[x]):
                        temp.append(message[x])

                    else:
                        break
                y = x + 1
                if re.match(regex_code2, message[x]):
                    temp = " ".join(temp)
                    if temp != []:
                        title = message[0] + ' ' + temp + ' ' + message[x]
                    else:
                        title = message[0] + ' ' + message[x]
                if y != 0:
                    message = message[y:len(message)]
                    description.append(message)
                    description = " ".join(message)
            if y == 0:
                message = message[1:len(message)]
                description.append(message)
                description = " ".join(message)
            embed = discord.Embed(title=title, description=description.replace('--', '\n\n'),
                                  color=0xf8a1a1)
            await ctx.channel.send(content=None, embed=embed)
        else:
            embed = discord.Embed(title="Instructions",
                                  description="-The title must be between double asterisks '**'\n"
                                              "-To enter a newline use '--'\n"
                                              "-Before any quotation mark use '\ ':heart:\n"
                                  , color=0xf8a1a1)
            await ctx.channel.send(content=None, embed=embed)
    except NameError:
        embed = discord.Embed(title="WHOOPSSSS SOMETHING WENT WRONG",
                              description="There must be a title between double asterisks.\n"
                                          "Before any quotation mark use a backslash.\n\n"
                                          "**TIP**: To enter a new line at the end of a sentence use double dash '--'."
                              , color=0xf8a1a1)
        await ctx.channel.send(content=None, embed=embed)


@client.command()
@commands.has_role(619601471838617612)
async def everyone(ctx):
    channel = client.get_channel(651097688447778817)
    await ctx.channel.send('@everyone')


@client.command()
async def stream(ctx):
    stream = discord.Streaming(name="My Stream", url="https://www.twitch.tv/spidertiff", twitch_name="spidertiff")
    await ctx.channel.send(stream.twitch_name)

client.run('NjQ2MDk3NTE1OTYzNDgyMTIz.XdqKdg.LOhPRWwLNt_XuDZW7--7VzmGOAE')
