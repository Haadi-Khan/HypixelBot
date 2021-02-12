import discord
import requests
import json
from discord.ext import commands

'''
TODO
JSON deletion to work
Monitor if a user is online (Implement with lastlogin > lastlogoff)

Longer Term: Grab player head as a thumbnail for embeds
'''

# I would use the .env variables but PIP IS STUPID AND IS ANNOYING ME AHHHHHHHHHHHHHH
TOKEN = 'NzYyMDcxOTY1ODE2OTc5NDU2.X3j00w.OninbzNFKbVaChQOmK9H5q0eAEk'
HYP_URL = 'https://api.hypixel.net/player?key=44a77889-afd3-47bf-8d79-0fc848ef6c43&name='
client = commands.Bot(command_prefix='s!')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command(name='sw')
async def skywars_stats(ctx, username):
    try:
        embed = discord.Embed(
            title='Skywars Stats',
            description='',
            color=discord.Colour.blue()
        )
        game_types = ['Solo Normal', 'Solo Insane', 'Team Normal', 'Team Insane']
        game_id = {'Solo Normal': 'solo_normal', 'Solo Insane': 'solo_insane', 'Team Normal': 'team_normal',
                   'Team Insane': 'team_insane'}
        data = requests.get(HYP_URL + username).json()['player']['stats']['SkyWars']
        embed.set_footer(text='From Hypixel API')
        # grab the head of the player
        # embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/304005401861423104/795aa39202d03e79ee8af4d4b03a46c3.png?size=128')
        for game_type in game_types:
            embed.add_field(name=game_type, value='​', inline=False)
            embed.add_field(name='Kills', value=data['kills_' + game_id[game_type]], inline=True)
            embed.add_field(name='Deaths', value=data['deaths_' + game_id[game_type]], inline=True)
            embed.add_field(name='W/L', value=round(
                data['wins_' + game_id[game_type]] / data['losses_' + game_id[game_type]], 2), inline=True)

        await ctx.send(embed=embed)
    except TypeError:
        await ctx.send('Invalid Username or has never played this gamemode')


@client.command(name='bw')
async def bedwars_stats(ctx, username):
    try:
        embed = discord.Embed(
            title='Bedwars Stats',
            description='',
            color=discord.Colour.blue()
        )
        game_types = ['Solo', 'Doubles', 'Threes', 'Fours']
        game_id = {'Solo': 'eight_one', 'Doubles': 'eight_two', 'Threes': 'four_three', 'Fours': 'four_four'}
        data = requests.get(HYP_URL + username).json()['player']['stats']['Bedwars']
        embed.set_footer(text='From Hypixel API')
        # grab the head of the player, will do this later
        # embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/304005401861423104/795aa39202d03e79ee8af4d4b03a46c3.png?size=128')
        for game_type in game_types:
            embed.add_field(name=game_type, value='​', inline=False)
            embed.add_field(name='Final Kills', value=data[game_id[game_type] + '_final_kills_bedwars'], inline=True)
            embed.add_field(name='Final Deaths', value=data[game_id[game_type] + '_final_deaths_bedwars'], inline=True)
            embed.add_field(name='FKDR', value=round(
                data[game_id[game_type] + '_final_kills_bedwars'] / data[game_id[game_type] + '_final_deaths_bedwars'],
                2), inline=True)
            embed.add_field(name='Beds Broken', value=data[game_id[game_type] + '_beds_broken_bedwars'], inline=True)
            embed.add_field(name='W/L', value=round(
                data[game_id[game_type] + '_wins_bedwars'] / data[game_id[game_type] + '_losses_bedwars'],
                2), inline=True)

        await ctx.send(embed=embed)
    except TypeError:
        await ctx.send('Invalid Username or has never played this gamemode')


def write_json(data, filename='player.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def remove_json(data, filename='player.json'):
    with open(filename, 'w') as dest_file:
        with open(data, 'r') as source_file:
            for line in source_file:
                element = json.loads(line.strip())
                if 'hours' in element:
                    del element['hours']
                dest_file.write(json.dumps(element))


@client.command(name='ping')
async def add_follow(ctx, username):
    with open('player.json') as player_file:
        data = json.load(player_file)
        temp = data['following']
        new_follow = {
            'username': username.lower(),
            'user_id': client.user.id,
        }
        temp.append(new_follow)
    write_json(data)
    await ctx.send('Signed up for player status')


@client.command(name='stop')
async def remove_follow(ctx, username):
    try:

        await ctx.send('No longer signed Up for player status')
    except TypeError:
        await ctx.send('Invalid Username')


client.run(TOKEN)
