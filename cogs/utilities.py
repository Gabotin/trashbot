import discord 
import pickle
import time, datetime
import json
import urllib, urllib.request
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

class utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.send_log = funcs.send_log
		self.log_prefix = ""

# 		========================

	@commands.command()
	async def about(self, ctx):
		await ctx.trigger_typing()
		try:
			guild_num = len(list(self.bot.guilds))
			user_num = 0
			for user in self.bot.users:
				if user.bot is True: continue 
				else: user_num += 1
			e_about = discord.Embed(title=f"trashbot | v{tt.v}", url=tt.website, description=f"{tt.desc}\n\n**bot name**: {self.bot.user}\n**bot ID**: `{self.bot.user.id}`", color=tt.clr['pink'])
			e_about.add_field(name="stats", value=f"servers: `{guild_num}`, users: `{user_num}`", inline=True)
			e_about.add_field(name=f"client uptime", value=f"{tt.uptime()}", inline=True)
			e_about.set_author(name=f"about trashbot", icon_url=tt.ico['info'])
			e_about.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			e_about.set_thumbnail(url=self.bot.user.avatar_url)
			await ctx.send(embed=e_about)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command(pass_context=True)
	async def ping(self, ctx):
		await ctx.trigger_typing()
		try:
			ptime = time.time()
			message = await ctx.send("⌛ ⠀pinging...")
			ping = round((time.time() - ptime) * 1000)
			await message.edit(content=f"🏓 ⠀pong! ({ping}ms)")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def invite(self, ctx):
		await ctx.trigger_typing()
		await ctx.send(tt.invite)

	@commands.command()
	@commands.guild_only()
	async def user(self, ctx, user: discord.User = None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		blacklist = pickle.load(open(tt.blacklist_pkl, "rb"))
		try:
			user_nick = ''; user_tag = ''; perm_tag = ''; trashbot_tag = ''
			if user.system: 
				user_tag = '[SYSTEM]'
			if user.bot:  
				user_tag = '[BOT]'
			if user.id == tt.owner_id:
				trashbot_tag += '\n`trashbot owner`'
			if user.id in tt.admins:
				trashbot_tag += '\n`trashbot admin`'
			if user.id in blacklist:
				trashbot_tag += '\n`trashbot blacklisted`'
			if user in ctx.guild.members:
				user = ctx.guild.get_member(user.id)
				if user.nick is not None: 
					user_nick = f'({user.nick})'
				if user.guild_permissions.administrator:
					perm_tag = '(admin)'
				if ctx.guild.owner == user: 
					perm_tag = '(owner)'
				e_user = discord.Embed(title=f"{user} {user_nick} {user_tag}", description=f"`{user.id}`\n**top role**: {user.top_role} {perm_tag}\n**joined**: __{user.joined_at.strftime(tt.time0)}__ ({'%d days' % (datetime.datetime.now() - user.joined_at).days})\n**created**: __{user.created_at.strftime(tt.time0)}__ ({'%d days' % (datetime.datetime.now() - user.created_at).days})\n{trashbot_tag}", color=user.color)
			else:
				e_user = discord.Embed(title=f"{user} {user_tag}", description=f"`{user.id}`\n**created**: __{user.created_at.strftime(tt.time0)}__ ({'%d days' % (datetime.datetime.now() - user.created_at).days})\n{trashbot_tag}", color=tt.clr['pink'])
			e_user.set_author(name=f"{user.name} :: user info", icon_url=tt.ico['info'])
			e_user.set_thumbnail(url=user.avatar_url)
			e_user.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_user)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	async def avatar(self, ctx, user: discord.User = None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		try:
			e_avatar = discord.Embed(color=ctx.message.author.top_role.colour)
			e_avatar.set_author(name=f"{user}'s avatar", icon_url=tt.ico['info'])
			e_avatar.set_image(url=user.avatar_url)
			e_avatar.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_avatar)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	async def server(self, ctx):
		await ctx.trigger_typing()
		try:
			e_server = discord.Embed(title=f"{ctx.guild.name}", description=f"`{ctx.guild.id}`\n**owner**: {ctx.guild.owner}\n**region**: {ctx.guild.region}\n**members**: {len(ctx.guild.members)}\n**roles**: {len(ctx.guild.roles)}\n**channels**: {len(ctx.guild.text_channels)} text + {len(ctx.guild.voice_channels)} voice\n**created**: __{ctx.guild.created_at.strftime(tt.time0)}__", color=tt.clr['pink'])
			e_server.set_author(name=f"{ctx.guild.name} :: server info", icon_url=tt.ico['info'])
			e_server.set_thumbnail(url=ctx.guild.icon_url)
			e_server.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_server)
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command(aliases=['mc'])
	async def mcserver(self, ctx):
		await ctx.trigger_typing()
		try:
			mcstats = json.loads(urllib.request.urlopen(f'https://api.mcsrvstat.us/2/{urllib.parse.quote(tt.mcserver)}').read().decode('utf8'))
			if mcstats['online'] == True:
				mc_offline = ''
				mc_players = f"\n\n{mcstats['players']['online']}/{mcstats['players']['max']} players online"
			else:
				mc_offline = "(offline)"
				mc_players = ''
			e_mcserver = discord.Embed(title=f"mc.elisttm.space {mc_offline}", url="https://elisttm.space/minecraft", description=f"{mcstats['version']} ({mcstats['software']}){mc_players}\n\n{mcstats['motd']['clean'][0]}\n{mcstats['motd']['clean'][1]}", color=tt.clr['pink'])
			e_mcserver.set_author(name=f"minecraft server info", icon_url=tt.ico['info'])
			e_mcserver.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_mcserver)
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def report(self, ctx, *, report:str):
		await ctx.trigger_typing()
		try:
			if len(report) > 1000:
				await ctx.send("⚠️ ⠀your report is too long!")
				return
			report = (tt.sanitize(text = report)).replace('`', '\`')
			report_msg = f"feedback recieved from '{ctx.author}' in '{ctx.guild.name}'"
			await self.send_log(self, log = f"{report_msg}\n{report}", prefix = self.log_prefix)
			await self.bot.get_user(tt.owner_id).send(f"{report_msg}\n> ```{report}```")
			await ctx.send("✅ ⠀your report has been submitted!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	@checks.is_server_or_bot_admin()
	async def massnick(self, ctx, *, nickname:str):
		await ctx.trigger_typing()
		try:
			mn_users = 0; mn_changed = 0
			if nickname == 'reset':
				nickname = None
			for member in ctx.guild.members: 
				mn_users += 1
			await ctx.send(f"⌛ ⠀attempting to change `{mn_users}` nicknames, please wait...")
			await self.send_log(self, log = f"changing '{mn_users}' nicknames to '{nickname}' in '{ctx.guild.name}'...", prefix = '[MASSNICK] ')
			for member in ctx.guild.members:
				await ctx.trigger_typing()
				try: 
					await member.edit(nick=nickname)
					mn_changed += 1
				except: 
					continue
			await ctx.send(f"✅ ⠀`{mn_changed}/{mn_users}` nicknames successfully changed!")
			await self.send_log(self, log = f"'{mn_changed}/{mn_users}' nicknames changed to '{nickname}' in '{ctx.guild.name}'!", prefix = '[MASSNICK] ')
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command(aliases=['purge'])
	@commands.guild_only()
	@commands.has_permissions(manage_messages = True)
	async def clear(self, ctx, clear:int):
		await ctx.trigger_typing()
		try:
			if (clear == 0) or (clear > 100): 
				await ctx.send("⚠️ ⠀invalid message amount! (must be between 1 - 100)")
				return
			await ctx.message.delete()
			await ctx.channel.purge(limit=(clear))
			await ctx.send(f"✅ ⠀cleared `{clear}` messages", delete_after=2)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.group(name = 'prefix')
	@commands.guild_only()
	async def prefix(self, ctx):
		await ctx.trigger_typing()
		if ctx.invoked_subcommand is None:
			try:
				custom_prefixes = pickle.load(open(tt.prefixes_pkl, "rb"))
				if ctx.guild.id not in custom_prefixes:
					await ctx.send("⚠️ ⠀no custom prefix for this guild. do `t!prefix set [prefix]` to create one!")
					return
				await ctx.send(f"ℹ️ ⠀this guild's custom prefix is '{custom_prefixes[ctx.guild.id]}'")
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	@prefix.command(name = 'set')
	@checks.is_server_or_bot_admin()
	async def prefix_set(self, ctx, prefix:str):
		try:
			if len(prefix) > 10:
				await ctx.send("⚠️ ⠀prefix too long! (max of 10 characters)")
				return
			custom_prefixes = pickle.load(open(tt.prefixes_pkl, "rb"))
			if ctx.guild.id in custom_prefixes:
				del custom_prefixes[ctx.guild.id]
			custom_prefixes[ctx.guild.id] = prefix
			pickle.dump(custom_prefixes, open(tt.prefixes_pkl, "wb"))
			await ctx.send(f"✅ ⠀custom prefix for this guild set to '{prefix}'!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@prefix.command(name = 'reset')
	@checks.is_server_or_bot_admin()
	async def prefix_reset(self, ctx):
		try:
			custom_prefixes = pickle.load(open(tt.prefixes_pkl, "rb"))
			if ctx.guild.id not in custom_prefixes:
				await ctx.send(f"❌ ⠀this guild does not have a custom prefix set!")
				return
			del custom_prefixes[ctx.guild.id]
			pickle.dump(custom_prefixes, open(tt.prefixes_pkl, "wb"))
			await ctx.send(f"✅ ⠀removed custom prefix for this guild!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

# 		========================

def setup(bot):
	bot.add_cog(utilities(bot))