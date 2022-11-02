import discord
from discord import Option
from discord.ext import commands
import os
import textwrap
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
import numpy

from config import config

class ImageManip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_font_size = 24
        self.default_paragraph_width = 24
        self.default_padding = 10
        self.path = os.path.join(config.ABSOLUTE_PATH, 'musicbot', 'commands')

        self.default_font = ImageFont.truetype(os.path.join(self.path, 'src', 'IndieFlower-Regular.ttf'), self.default_font_size)

    def find_coeffs(self, pa, pb):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

        A = numpy.matrix(matrix, dtype=float)
        B = numpy.array(pb).reshape(8)

        res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
        return numpy.array(res).reshape(8)

    @commands.command(name="nijisign", description=config.HELP_NIJISIGN_LONG, help=config.HELP_NIJISIGN_SHORT)
    async def nijisign(self, ctx: commands.Context, *, text: str = None):
        text = text or f"Hello {ctx.author.name}! Nijika here!"
        
        para = textwrap.wrap(text, width=24)
        bytes = BytesIO()
        MAX_W, MAX_H = 320, 220
        text_img = Image.new('RGB', (MAX_W, MAX_H), (232, 232, 232))
        draw = ImageDraw.Draw(text_img)

        current_h = (MAX_H - ((self.default_font_size + self.default_padding) * len(para) - self.default_padding)) / 2
        for line in para:
            w, h = draw.textsize(line, font=self.default_font)
            draw.text(((MAX_W - w) / 2, current_h), line, font=self.default_font, fill=(0, 0, 0, 0))
            current_h += h + self.default_padding

        sign = Image.open(f'{self.path}/src/nijisign.png')

        output = Image.new('RGBA', (480,640), (231, 232, 231))
        output.paste(text_img, (70,360))
        output.paste(sign, (0,0), mask=sign)

        output.save(bytes, format="PNG")
        bytes.seek(0)
        dfile = discord.File(bytes, filename="sign.png")

        await ctx.send(file=dfile)

    @commands.command(name="bocchisign", description=config.HELP_BOCCHISIGN_LONG, help=config.HELP_BOCCHISIGN_SHORT)
    async def bocchisign(self, ctx, *, text: str = None):
        text = text or f"I'm a bad bot host"

        para = textwrap.wrap(text, width=24)
        MAX_W, MAX_H = 280, 220
        text_img = Image.new('RGB', (MAX_W, MAX_H), (232, 232, 232))
        draw = ImageDraw.Draw(text_img)
        bytes = BytesIO()

        current_h = (MAX_H - ((self.default_font_size + self.default_padding) * len(para) - self.default_padding)) / 2
        for line in para:
            w, h = draw.textsize(line, font=self.default_font)
            draw.text(((MAX_W - w) / 2, current_h), line, font=self.default_font, fill=(0, 0, 0, 0))
            current_h += h + self.default_padding
            
        coeffs = self.find_coeffs(
            [(0, 0), (280, 45), (245, 216), (5, 160)],
            [(0, 0), (MAX_W, 0), (MAX_W, MAX_H), (0, MAX_H)])

        text_img = text_img.transform((MAX_W, MAX_H), Image.PERSPECTIVE, coeffs, Image.BICUBIC, fillcolor=(232, 232, 232))

        sign = Image.open(f'{self.path}/src/bocchisign.png')

        output = Image.new('RGBA', (400,600), (231, 232, 231))
        output.paste(text_img, (45,315))
        output.paste(sign, (0,0), mask=sign)

        output.save(bytes, format="PNG")
        bytes.seek(0)
        dfile = discord.File(bytes, filename="bocchisign.png")

        await ctx.send(file=dfile)
        
def setup(bot):
    bot.add_cog(ImageManip(bot))
