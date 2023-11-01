import discord
import asyncio
from MuteAll.utils import can_do, get_affected_users


async def do(task="mute", members=None):
    if members is None:
        # members = []
        return
    
    print(members)

    for member in members:
        match task:
            case "mute":
                await member.edit(mute=True)
            case "unmute":
                await member.edit(mute=False)
            case "end":
                await member.edit(mute=False)
            case "deafen":
                await member.edit(deafen=True)
            case "undeafen":
                await member.edit(deafen=False)
            case "all":
                await member.edit(mute=True)
                await member.edit(deafen=True)
            case "unall":
                await member.edit(mute=False)
                await member.edit(deafen=False)


async def do_mute(ctx: discord.ApplicationContext, mentions):
    canDo = can_do(ctx, requiredPermissions=["mute"])
    if canDo != "OK":
        return await ctx.respond(canDo)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(task="mute", members=members)
    await ctx.respond("👍")


async def do_unmute(ctx, mentions):

    canDo = can_do(ctx)
    if canDo != "OK":
        return await ctx.respond(canDo)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(task="unmute", members=members)
    await ctx.respond("👍")

async def do_stfu(ctx: discord.ApplicationContext, mentions):
    canDo = can_do(ctx)
    if canDo != "OK":
        return await ctx.respond(canDo)
    
    await ctx.defer()
    
    shot_caller_role = None

    for role in ctx.guild.roles:
        if role.name == 'Shot Caller':
            shot_caller_role = role.id

    members = []
    channel = ctx.guild.get_channel(ctx.author.voice.channel.id)
    channel_members = await asyncio.gather(*[member.guild.fetch_member(member.id) for member in channel.members])
    for member in channel_members:
        if shot_caller_role not in [role.id for role in member.roles]:
            members.append(member)

        await do(task="mute", members=members)
    await ctx.respond('👍')


async def do_deafen(ctx, mentions):
    canDo = can_do(ctx, requiredPermissions=["deafen"])
    if canDo != "OK":
        return await ctx.respond(canDo)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(task="deafen", members=members)
    await ctx.respond("👍")


async def do_undeafen(ctx, mentions):

    canDo = can_do(ctx)
    if canDo != "OK":
        return await ctx.respond(canDo)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(task="undeafen", members=members)
    await ctx.respond("👍")


async def do_all(ctx, mentions):

    canDo = can_do(ctx, requiredPermissions=["mute", "deafen"])
    if canDo != "OK":
        return await ctx.respond(canDo)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(task="all", members=members)
    await ctx.respond("👍")


async def do_unall(ctx, mentions):

    canDo = can_do(ctx)
    if canDo != "OK":
        return await ctx.respond(canDo)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(task="unall", members=members)
    await ctx.respond("👍")


async def add_reactions(ctx, emojis):

    canDo = can_do(ctx, requiredPermissions=["mute", "deafen"])
    if canDo != "OK":
        return await ctx.respond(canDo)

    embed = discord.Embed()
    embed.set_author(name="Reaction Commands")
    embed.add_field(name=emojis["MUTE"], value="mute")
    embed.add_field(name=emojis["UNMUTE"], value="un-mute")
    embed.add_field(name=emojis["DEAFEN"], value="deafen")
    embed.add_field(name=emojis["UNDEAFEN"], value="un-deafen")
    embed.add_field(name=emojis["ALL"], value="mute + deafen")
    embed.add_field(name=emojis["UNALL"], value="un-mute + un-deafen")

    await ctx.respond("React with an emoji below!")

    message = await ctx.send(embed=embed)

    for emoji in emojis.values():
        await message.add_reaction(emoji)
