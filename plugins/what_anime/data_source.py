# -*- coding: utf-8 -*-
import aiohttp


class QueryError(Exception):
    def __str__(self):
        return '未查询到相关结果'


class TraceMeo:
    def __init__(self, pic_url):
        self.pic_url = pic_url

    async def get_result(self, proxy: str = '') -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.trace.moe/search?anilistInfo&url={self.pic_url}', proxy=proxy) as resp:
                result = await resp.json()
                if result['error'] != '':
                    raise QueryError
                else:
                    return result

    async def get_result_formatted(self, proxy: str = '') -> str:
        try:
            result = await self.get_result(proxy)
            max_results = len(result['result']) if len(result['result']) < 5 else 5
            ret = '智乃酱为您找到了以下结果：\n'
            for anime in result['result'][:max_results]:
                ret += '--------------------------\n'

                # 获取番剧名称
                synonyms = anime['anilist']['synonyms']
                for alias in synonyms:
                    _count_ch = 0
                    for word in alias:
                        if '\u4e00' <= word <= '\u9fff':
                            _count_ch += 1
                    if _count_ch > 3:
                        anime_name = alias
                        break
                else:
                    anime_name = anime['anilist']['title']['native']
                ret += f'{anime_name}\n'

                # 获取集数
                episode = anime['episode']
                if episode is not None:
                    ret += f'集数: {episode}\n'

                # 获取时间码
                from_m, from_s = divmod(int(anime["from"]), 60)
                to_m, to_s = divmod(int(anime["to"]), 60)
                ret += f'时间: {from_m}:{from_s} ~ {to_m}:{to_s}\n'

                # 获取相似度
                similarity = anime["similarity"]
                ret += '相似度:{:.2%}\n'.format(similarity)

                # 获取图片
                # NOTE: 有可能出现里番截图，如需要自行取消注释
                # ret += f'[CQ:image,file={anime["image"]}]'

            return ret

        except QueryError:
            return '未查询到相关结果呢~换张图试试？'
