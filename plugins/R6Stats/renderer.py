"""
渲染战绩图片的模块
"""
# -*- coding: utf-8 -*-
import os
import random

import aiohttp

from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


class StatsRenderer:
    def __init__(self, data: dict, proxy: str = ''):
        self.data = data
        self.proxy = proxy

    async def render(self):
        # 加载背景图
        background_list = os.listdir('./plugins/R6Stats/resources/backgrounds')
        background = random.sample(background_list, 1)[0]
        image = Image.open(f'./plugins/R6Stats/resources/backgrounds/{background}')

        # 加载面板图
        panel_layer = Image.open('./plugins/R6Stats/resources/panel_layer.png')

        # 叠加面板图层
        image.alpha_composite(panel_layer)

        # 渲染头像
        async with aiohttp.ClientSession() as session:
            async with session.get(self.data['avatar_url'], proxy=self.proxy) as resp:
                avatar = Image.open(BytesIO(await resp.read()))
        # 圆角处理
        circle = Image.new('L', (20 * 2, 20 * 2), 0)  # 创建黑色方形
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, 20 * 2, 20 * 2), fill=255)  # 黑色方形内切白色圆形
        avatar = avatar.convert("RGBA")
        w, h = avatar.size
        # 创建一个alpha层，存放四个圆角，使用透明度切除圆角外的图片
        alpha = Image.new('L', avatar.size, 255)
        alpha.paste(circle.crop((0, 0, 20, 20)), (0, 0))  # 左上角
        alpha.paste(circle.crop((20, 0, 20 * 2, 20)), (w - 20, 0))  # 右上角
        alpha.paste(circle.crop((20, 20, 20 * 2, 20 * 2)), (w - 20, h - 20))  # 右下角
        alpha.paste(circle.crop((0, 20, 20, 20 * 2)), (0, h - 20))  # 左下角
        avatar.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
        avatar = avatar.resize((150, 150))
        image.alpha_composite(avatar, (88, 76))

        # 渲染ID
        id_font = ImageFont.truetype('./plugins/R6Stats/resources/fonts/lexend-deca-v1-latin-regular.ttf',
                                     75)
        sub_id_font = ImageFont.truetype('./plugins/R6Stats/resources/fonts/HarmonyOS_Sans_SC_Regular.ttf',
                                         30)
        draw = ImageDraw.Draw(image)
        draw.text((280, 75), self.data['username'], font=id_font)
        draw.text((285, 186), f'等级: {self.data["level"]}  |  UID: {self.data["uuid"].upper()}',
                  font=sub_id_font, fill=(180, 180, 180))

        # 渲染title段位
        rank = Image.open(f'./plugins/R6Stats/resources/rank/{self.data["rank"]["rank"]["id"]}.png')
        rank = rank.resize((104, 128))
        image.alpha_composite(rank, (1380, 85))
        rank_font = ImageFont.truetype('./plugins/R6Stats/resources/fonts/HarmonyOS_Sans_SC_Regular.ttf',
                                       50)
        draw.text((1510, 88), self.data["rank"]["rank"]['name'], font=rank_font)
        draw.text((1513, 148),
                  f'{self.data["rank"]["MMR"]} MMR - {self.data["rank"]["wins"]} W {self.data["rank"]["losses"]} L'
                  f'\n区服: {self.data["rank"]["region"].upper()}',
                  font=sub_id_font, fill=(180, 180, 180))

        # 数据渲染
        data_font = ImageFont.truetype('./plugins/R6Stats/resources/fonts/lexend-deca-v1-latin-regular.ttf', 42)

        # 全局数据渲染
        # 第一行
        draw.text((83, 455), str(self.data['general']['kd']), font=data_font)
        draw.text((279, 455), str(self.data['general']['win_rate']), font=data_font)
        draw.text((454, 455), str(self.data['general']['kills_per_game']), font=data_font)
        draw.text((675, 455), str(self.data['general']['kills']), font=data_font)
        draw.text((859, 455), str(self.data['general']['wins']), font=data_font)
        draw.text((1056, 455), str(self.data['general']['games_played']), font=data_font)
        # 第二行
        draw.text((83, 552), str(self.data['general']['deaths']), font=data_font)
        draw.text((279, 552), str(self.data['general']['losses']), font=data_font)
        draw.text((454, 552), str(self.data['general']['playtime']), font=data_font)
        draw.text((675, 552), str(self.data['general']['dbnos']), font=data_font)
        draw.text((859, 552), str(self.data['general']['rank_kd']), font=data_font)
        draw.text((1056, 552), str(self.data['general']['casual_kd']), font=data_font)

        # 多人游戏数据渲染
        # 第一行
        draw.text((89, 792), str(self.data['multi']['kills']), font=data_font)
        draw.text((283, 792), str(self.data['multi']['blind_kills']), font=data_font)
        draw.text((459, 792), str(self.data['multi']['melee_kills']), font=data_font)
        draw.text((675, 792), str(self.data['multi']['penetration_kills']), font=data_font)
        draw.text((862, 792), str(self.data['multi']['headshots']), font=data_font)
        draw.text((1059, 792), str(self.data['multi']['headshots_rate']), font=data_font)
        # 第二行
        draw.text((89, 889), str(self.data['multi']['assists']), font=data_font)
        draw.text((283, 889), str(self.data['multi']['revives']), font=data_font)
        draw.text((459, 889), str(self.data['multi']['suicides']), font=data_font)
        draw.text((676, 889), str(self.data['multi']['barricades_deployed']), font=data_font)
        draw.text((865, 889), str(self.data['multi']['reinforcements_deployed']), font=data_font)
        draw.text((1059, 889), str(self.data['multi']['rappel_breaches']), font=data_font)

        # 排位数据渲染
        rank = rank.resize((122, 150))
        image.alpha_composite(rank, (1333, 438))
        rank_font = ImageFont.truetype('./plugins/R6Stats/resources/fonts/lexend-deca-v1-latin-regular.ttf', 55)
        draw.text((1510, 505), str(self.data['rank']['MMR']), font=rank_font)
        draw.text((1688, 505), str(self.data['rank']['max_MMR']), font=rank_font)
        draw.text((1310, 687), str(self.data['rank']['wins']), font=rank_font)
        draw.text((1486, 687), str(self.data['rank']['losses']), font=rank_font)
        draw.text((1665, 687), str(self.data['rank']['win_rate']), font=rank_font)
        draw.text((1310, 825), str(self.data['rank']['kills']), font=rank_font)
        draw.text((1486, 825), str(self.data['rank']['deaths']), font=rank_font)
        draw.text((1665, 825), str(self.data['rank']['kd']), font=rank_font)

        # 更新数据时间
        update_time_font = ImageFont.truetype(
            './plugins/R6Stats/resources/fonts/HarmonyOS_Sans_SC_Regular.ttf', 25)
        draw.text((63, 996), '数据更新时间: ' + self.data['last_updated'], font=update_time_font)

        img_data = BytesIO()
        image.save(img_data, format='PNG')
        return img_data
