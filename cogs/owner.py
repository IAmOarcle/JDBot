from discord.ext import commands, menus
import utils
import random , discord , aiohttp , os , aiosqlite, importlib, mystbin
import traceback, textwrap

class Owner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(brief="a command to send mail")
  async def mail(self,ctx,*,user: utils.BetterUserconverter=None):
    if user is None:
      await ctx.reply("User not found, returning Letter")
      user = ctx.author
    if user:
      await ctx.reply("Please give me a message to use.")
      message = await self.bot.wait_for("message",check =utils.check(ctx))
      embed_message = discord.Embed(title=message.content, timestamp=(message.created_at), color=random.randint(0, 16777215))
      embed_message.set_author(name=f"Mail from: {ctx.author}",icon_url=(ctx.author.avatar_url))
      embed_message.set_footer(text = f"{ctx.author.id}")
      embed_message.set_thumbnail(url = "https://i.imgur.com/1XvDnqC.png")
      if (user.dm_channel is None):
        await user.create_dm()
      try:
        await user.send(embed=embed_message)
      except:
        user = ctx.author
        await user.send(content="Message failed. sending",embed=embed_message)
        embed_message.add_field(name="Sent To:",value=str(user))
      await self.bot.get_channel(738912143679946783).send(embed=embed_message)

  @commands.command()
  async def load(self,ctx,*,cog=None):
    if cog:
      try:
        self.bot.load_extension(cog)
      except Exception as e:
        await ctx.send(e)
      await ctx.send("Loaded cog(see if there's any errors)")
    if cog is None:
      await ctx.send("you can't ask to load no cogs.")
  
  @commands.command()
  async def reload(self,ctx,*,cog=None):
    if cog:
      if cog == "all":
        for x in list(self.bot.extensions):
          try:
            self.bot.reload_extension(x)
          except commands.errors.ExtensionError as e:
            await ctx.send(e)
        await ctx.send("done reloading all cogs(check for any errors)")
      if cog != "all":
        try:
          self.bot.reload_extension(cog)
        except commands.errors.ExtensionError as e:
          await ctx.send(e)
      await ctx.send("Cog reloaded :D (check for any errors)")
    if cog is None:
      await ctx.send("you can't ask to reload no cogs")
  
  @commands.command()
  async def unload(self,ctx,*,cog=None):
    if cog:
      try:
        self.bot.unload_extension(cog)
      except commands.errors.ExtensionError as e:
        await ctx.send(e)
      await ctx.send("Cog should be unloaded just fine :D.(check any errors)")
    if cog is None:
      await ctx.send("you can't ask to reload no cogs")

  @commands.command()
  async def shutdown(self,ctx):
    await ctx.send("shutdown/logout time happening.")
    await self.bot.close()

  async def cog_check(self, ctx):
    return await self.bot.is_owner(ctx.author)

  async def cog_command_error(self, ctx, error):
    if not ctx.command and ctx.command.has_error_handler():
      await ctx.send(error)

  @commands.command(brief="Changes Bot Status(Owner Only)")
  async def status(self , ctx , * , args=None):
    if await self.bot.is_owner(ctx.author):
      if args:
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity= discord.Activity(type=discord.ActivityType.watching,name=args))
      if args is None:
        await self.bot.change_presence(status=discord.Status.do_not_disturb)
    if await self.bot.is_owner(ctx.author) is False:
      await ctx.send("That's an owner only command")
  
  @commands.command(brief="Only owner command to change bot's nickname")
  async def change_nick(self, ctx ,*, name=None):
    if await self.bot.is_owner(ctx.author):
      if isinstance(ctx.channel, discord.TextChannel):
        await ctx.send("Changing Nickname")
        try:
          await ctx.guild.me.edit(nick=name)
        except discord.Forbidden:
          await ctx.send("Appears not to have valid perms")
      if isinstance(ctx.channel,discord.DMChannel):
        await ctx.send("You can't use that in Dms.")
      
    if await self.bot.is_owner(ctx.author) is False:
      await ctx.send("You can't use that command")

  class ServersEmbed(menus.ListPageSource):
    async def format_page(self, menu, item):
      embed = discord.Embed(title="Servers:",description=item,color=random.randint(0, 16777215))
      return embed
  
  @commands.command(brief="a command to give a list of servers(owner only)",help="Gives a list of guilds(Bot Owners only)")
  async def servers(self,ctx):
    if await self.bot.is_owner(ctx.author):

      pag = commands.Paginator()
      for g in self.bot.guilds:
       pag.add_line(f"[{len(g.members)}/{g.member_count}] **{g.name}** (`{g.id}`) | {(g.system_channel or g.text_channels[0]).mention}")

      pages = [page.strip("`") for page in pag.pages]
      menu = menus.MenuPages(self.ServersEmbed(pages, per_page=1),delete_message_after=True)
      await menu.start(ctx,channel=ctx.author.dm_channel)
      
    if await self.bot.is_owner(ctx.author) is False:
      await ctx.send("You can't use that it's owner only")

  @commands.command(brief="only works with JDJG, but this command is meant to send updates to my webhook")
  async def webhook_update(self,ctx,*,args=None):
    if await self.bot.is_owner(ctx.author):
      if args:
        if isinstance(ctx.channel, discord.TextChannel):
          await ctx.message.delete()

          session = self.bot.session
          webhook=discord.Webhook.from_url(os.environ["webhook1"], adapter=discord.AsyncWebhookAdapter(session))
          embed=discord.Embed(title="Update",color=(35056),timestamp=(ctx.message.created_at))
          embed.add_field(name="Update Info:",value=args)
          embed.set_author(name="JDJG's Update",icon_url='https://i.imgur.com/pdQkCBv.png')
          embed.set_footer(text="JDJG's Updates")
          await webhook.execute(embed=embed)
        
          session = self.bot.session
          webhook=discord.Webhook.from_url(os.environ["webhook99"], adapter=discord.AsyncWebhookAdapter(session))
          embed=discord.Embed(title="Update",color=(35056),timestamp=(ctx.message.created_at))
          embed.add_field(name="Update Info:",value=args)
          embed.set_author(name="JDJG's Update",icon_url='https://i.imgur.com/pdQkCBv.png')
          embed.set_footer(text="JDJG's Updates")
          await webhook.execute(embed=embed)
      if args is None:
        await ctx.send("You sadly can't use it like that.")
    if await self.bot.is_owner(ctx.author) is False:
      await ctx.send("You can't use that")

  class mutualGuildsEmbed(menus.ListPageSource):
    async def format_page(self, menu, item):
      embed = discord.Embed(title="Servers:",description=item,color=random.randint(0, 16777215))
      return embed

  @commands.command(brief="Commands to see what guilds a person is in.")
  async def mutualguilds(self,ctx,*,user: utils.BetterUserconverter=None):
    user = user or ctx.author
    pag = commands.Paginator()

    for g in user.mutual_guilds:
      pag.add_line(f"{g}")

    pages = [page.strip("`") for page in pag.pages]
    pages = pages or ["No shared servers"]

    menu = menus.MenuPages(self.mutualGuildsEmbed(pages, per_page=1),delete_message_after=True)
    await menu.start(ctx,channel=ctx.author.dm_channel)

  @commands.command(brief="A command to add sus_users with a reason")
  async def addsus(self,ctx,*,user: utils.BetterUserconverter=None):
    if user is None:
      await ctx.send("can't have a user be none.")

    if user:
      await ctx.reply("Please give me a reason why:")
      reason = await self.bot.wait_for("message",check= utils.check(ctx))
      cur = await self.bot.sus_users.cursor()
      await cur.execute("INSERT INTO sus_users VALUES (?, ?)", (user.id, reason.content))
      await self.bot.sus_users.commit()
      await cur.close()
      await ctx.send("added sus users, succesfully")

  @commands.command(brief="a command to remove sus users.")
  async def removesus(self,ctx,*,user: utils.BetterUserconverter=None):
    if user is None:
      await ctx.send("You can't have a none user.")

    if user:
      cur = await self.bot.sus_users.cursor()
      await cur.execute("DELETE FROM sus_users WHERE user_id = ?", (user.id,))
      await self.bot.sus_users.commit()
      await cur.close()
      await ctx.send("Removed sus users.")

  class SusUsersEmbed(menus.ListPageSource):
    async def format_page(self, menu, item):
      embed=discord.Embed(title = "Users Deemed Suspicious by JDJG Inc. Official", color=random.randint(0, 16777215))
      embed.add_field(name = f"User ID : {item[0]}", value = f"**Reason :** {item[1]}", inline = False)
      return embed

  @commands.command(brief="a command to grab all in the sus_users list")
  async def sus_users(self,ctx):
    cur = await self.bot.sus_users.cursor()
    cursor = await cur.execute("SELECT * FROM SUS_USERS;")
    sus_users = await cursor.fetchall()
    await cur.close()
    await self.bot.sus_users.commit()  
    menu = menus.MenuPages(self.SusUsersEmbed(sus_users, per_page=1),delete_message_after=True)
    await menu.start(ctx)

  @commands.command()
  async def update_sus(self,ctx):
    await self.bot.sus_users.commit()
    await ctx.send("Updated SQL boss.")

  @update_sus.error
  async def update_sus_error(self,ctx,error):
    await ctx.send(error)

  @commands.command(aliases=["bypass_command"])
  async def command_bypass(self,ctx,user: utils.BetterUserconverter=None,*,command=None):
    #make sure to swap to autoconverter if it gets added.
    user = user or ctx.author
    if command:
      command_wanted=self.bot.get_command(command)
      if command_wanted:
        await ctx.send(f"{command_wanted.name} now accessible for the {user} for one command usage!")
        self.bot.special_access[user.id]=command_wanted.name
      if command_wanted is None:
        await ctx.send("Please specify a valid command.")
    if command is None:
      await ctx.send("select a command :(")

  @commands.command()
  async def leave_guild(self, ctx, *, guild: discord.Guild = None):
    guild = guild or ctx.guild
    if guild is None: return await ctx.send("Guild is None can't do anything.")
    print(guild)

  
  @commands.command()
  async def aioinput_test(self, ctx, *, args = None):
    args = args or "Test"

    result=await self.bot.loop.run_in_executor(None, input, (f"{args}:"))
    await ctx.send(f"Result of the input was {result}")

  @commands.command(brief="a powerful owner tool to reload local files that aren't reloadable.")
  async def reload_basic(self, ctx, *, args = None):
    if args is None:await ctx.send("Can't reload module named None")

    if args:
      try: module = importlib.import_module(name=args)
      except Exception as e: return await ctx.send(e)

      try: value=importlib.reload(module)
      except Exception as e: return await ctx.send(e)

      await ctx.send(f"Sucessfully reloaded {value.__name__} \nMain Package: {value.__package__}")


  @commands.command(brief="backs up a channel and then sends it into a file or mystbin")
  async def channel_backup(self, ctx):

    messages = await ctx.channel.history(limit=None, oldest_first=True).flatten()

    page = "\n".join(f"{msg.author} ({['User', 'Bot'][msg.author.bot]}) : {msg.content}" for msg in messages)

    mystbin_client = mystbin.Client(session=self.bot.session)
    paste = await mystbin_client.post(page)

    await ctx.author.send(content=f"Added text file to mystbin: \n{paste.url}")

  @channel_backup.error
  async def channel_backup_error(self, ctx, error):
    etype = type(error)
    trace = error.__traceback__

    values=''.join(map(str,traceback.format_exception(etype, error, trace)))
 
    pages = textwrap.wrap(values, width = 1992)

    menu = menus.MenuPages(utils.ErrorEmbed(pages, per_page=1),delete_message_after=True)

    await menu.start(ctx,channel=ctx.author.dm_channel)

    mystbin_client = mystbin.Client(session=self.bot.session)
    paste = await mystbin_client.post(values)

    await ctx.send(f"Traceback: {paste.url}")
     


def setup(client):
  client.add_cog(Owner(client))
