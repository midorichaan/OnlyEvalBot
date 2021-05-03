from discord.ext import commands

import io
import textwrap
import traceback
from contextlib import redirect_stdout

class command(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.result = ""
    
    #utils escape `py
    def escape_quote(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')
    
    #救世主evalコマンド
    @commands.command(name="eval", pass_context=True)
    @commands.is_owner()
    async def eval_(self, ctx, *, body: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'self': self,
            '_': self.result
        }

        env.update(globals())

        body = self.escape_quote(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            
            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self.result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

def setup(bot):
    bot.add_cog(command(bot))
