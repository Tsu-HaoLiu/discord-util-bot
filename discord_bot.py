from dotenv import dotenv_values

from utils.unshortner import unshortner
from utils.yt_dler import download_video
from utils.utils import delete_file, file_size, convert_bytes_to_mb, create_formatted_reply

import discord
from discord.ext import commands

config = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True
input_channel = int(config['INPUT_CHANNEL'])
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    # Allow the bot to process commands
    await bot.process_commands(message)

    # Check if the message starts with the command prefix and is not sent by a bot
    if message.content.startswith(bot.command_prefix) and not message.author.bot:
        await message.delete()

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def s(ctx, url: str, *details):
    """Unshortens tiktok url
    :param ctx:
    :param url:
    :param details: (optional) additional detail that is appended as text to the links
    """
    unshortned_url = unshortner(url)
    send_url = unshortned_url['cleaned']

    if unshortned_url['cleaned'].find('tiktok') != -1:
        send_url = unshortned_url['cleaned'].split('?')[0]

    compiled_sent_message = create_formatted_reply(ctx, send_url, details)

    await ctx.send(compiled_sent_message)

@bot.command()
async def sc(ctx, url: str, *details):
    """Sends to a custom discord channel set in .env 
    :param ctx:
    :param url:
    :param details: (optional) additional detail that is appended as text to the links
    """
    channel = bot.get_channel(input_channel)
    unshortned_url = unshortner(url)
    send_url = unshortned_url['cleaned']

    if unshortned_url['cleaned'].find('tiktok') != -1:
        send_url = unshortned_url['cleaned'].split('?')[0]

    compiled_sent_message = create_formatted_reply(ctx, send_url, details)

    if channel is not None:
        await channel.send(compiled_sent_message)
    else:
        await ctx.send(compiled_sent_message)

@bot.command()
async def sfull(ctx, url: str):
    unshortned_url = unshortner(url)
    await ctx.send(unshortned_url['redirect_history'])

@bot.command()
async def d(ctx, url: str, *details):
    unshortned_url = unshortner(url)
    send_url = unshortned_url['cleaned']

    if unshortned_url['cleaned'].find('tiktok') != -1:
        send_url = unshortned_url['cleaned'].split('?')[0]

    compiled_sent_message = create_formatted_reply(ctx, send_url, details, hide_embed=True)
    mp4_file = download_video(send_url, fmt='mp4', ffmpeg_location=config['FFMPEG_LOCATION'])

    # 1024*1024
    # 10_480_000 bytes = 9.995MB
    # https://support.discord.com/hc/en-us/articles/25444343291031-File-Attachments-FAQ
    downloaded_file_size = file_size(mp4_file)
    if downloaded_file_size <= 10_480_000:
        file = discord.File(mp4_file)
        delete_file(mp4_file)
        await ctx.send(content=compiled_sent_message, file=file)
    else:
        await ctx.send(f'[Failed] Filesize: {convert_bytes_to_mb(downloaded_file_size)}\n{compiled_sent_message}')

@bot.command()
async def ds(ctx, url: str, *details):
    """Unshortens tiktok url then downloads the video and convert to mp3 and reply with upload.
    :param ctx:
    :param url:
    :param details: (optional) additional detail that is appended as text to the links
    """
    unshortned_url = unshortner(url)
    send_url = unshortned_url['cleaned']

    if unshortned_url['cleaned'].find('tiktok') != -1:
        send_url = unshortned_url['cleaned'].split('?')[0]

    mp3_file = download_video(send_url, fmt='mp3', ffmpeg_location=config['FFMPEG_LOCATION'])
    file = discord.File(mp3_file)
    delete_file(mp3_file)  # delete local copy of file

    compiled_sent_message = create_formatted_reply(ctx, send_url, details)

    await ctx.send(content=compiled_sent_message, file=file)


bot.run(config['TOKEN'])
