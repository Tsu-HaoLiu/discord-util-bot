from dotenv import dotenv_values

from utils.unshortner import unshortner
from utils.yt_dler import download_video

import discord
from discord.ext import commands

config = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True
input_channel = int(config['INPUT_CHANNEL'])
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    # Check if the message starts with the command prefix and is not sent by a bot
    if message.content.startswith(bot.command_prefix) and not message.author.bot:
        await message.delete()

    # Allow the bot to process commands
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def s(ctx, url: str):
    unshortned_url = unshortner(url)
    send_url = unshortned_url['cleaned']

    if unshortned_url['cleaned'].find('tiktok') != -1:
        send_url = unshortned_url['cleaned'].split('?')[0]

    await ctx.send(send_url)

@bot.command()
async def sc(ctx, url: str):
    channel = bot.get_channel(input_channel)
    unshortned_url = unshortner(url)
    send_url = unshortned_url['cleaned']

    if unshortned_url['cleaned'].find('tiktok') != -1:
        send_url = unshortned_url['cleaned'].split('?')[0]

    if channel is not None:
        await channel.send(send_url)
    else:
        await ctx.send(send_url)

@bot.command()
async def sfull(ctx, url: str):
    unshortned_url = unshortner(url)
    await ctx.send(unshortned_url['redirect_history'])

@bot.command()
async def d(ctx, url: str):
    unshortned_url = unshortner(url)
    send_url = unshortned_url['cleaned']

    if unshortned_url['cleaned'].find('tiktok') != -1:
        send_url = unshortned_url['cleaned'].split('?')[0]

    # mp4_file = download_video(send_url, fmt='mp4', ffmpeg_location=config['FFMPEG_LOCATION'])
    # file = discord.File(mp4_file)

    await ctx.send(f'Discord upload size is too small, here is the unshortned url instead: {send_url}')

@bot.command()
async def ds(ctx, url: str):
    unshortned_url = unshortner(url)
    send_url = unshortned_url['cleaned']

    if unshortned_url['cleaned'].find('tiktok') != -1:
        send_url = unshortned_url['cleaned'].split('?')[0]

    mp3_file = download_video(send_url, fmt='mp3', ffmpeg_location=config['FFMPEG_LOCATION'])
    file = discord.File(mp3_file)

    await ctx.send(file=file)


bot.run(config['TOKEN'])
