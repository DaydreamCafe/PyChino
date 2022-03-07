"""
从R6Stats获取数据并重新格式化数据的模块
"""
# -*- coding: utf-8 -*-
import aiohttp


async def get_stats(game_id: str, proxy: str = ''):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://r6stats.com/api/player-search/{game_id}/pc', proxy=proxy) as resp:
            original_stats = (await resp.json())['data'][0]

    try:
        general_kd = int(
            original_stats['genericStats']['general']['kills'] /
            original_stats['genericStats']['general']['deaths'] * 100) / 100
    except ZeroDivisionError:
        general_kd = 0

    try:
        general_win_rate = str(int(
            original_stats['genericStats']['general']['wins'] /
            original_stats['genericStats']['general']['games_played'] * 10000) / 100) + '%'
    except ZeroDivisionError:
        general_win_rate = '00.00%'

    try:
        general_win_kills_per_game = int(
            original_stats['genericStats']['general']['kills'] /
            original_stats['genericStats']['general']['games_played'] * 10) / 10
    except ZeroDivisionError:
        general_win_kills_per_game = 0

    try:
        general_playtime = str(int(original_stats['genericStats']['general']['playtime'] / 3600 * 10) / 10) + 'h'
    except ZeroDivisionError:
        general_playtime = '0h'

    try:
        general_rank_kd = str(int(
            original_stats['genericStats']['queue']['ranked']['kills'] /
            original_stats['genericStats']['queue']['ranked']['deaths'] * 100) / 100)
    except ZeroDivisionError:
        general_rank_kd = 0

    try:
        general_casual_kd = str(int(
            original_stats['genericStats']['queue']['casual']['kills'] / original_stats['genericStats']['queue']
            ['casual']['deaths'] * 100) / 100)
    except ZeroDivisionError:
        general_casual_kd = 0

    try:
        multi_headshots_rate = str(int(
            original_stats['genericStats']['general']['headshots'] /
            original_stats['genericStats']['general']['kills'] * 10000) / 100) + '%'
    except ZeroDivisionError:
        multi_headshots_rate = '00.00%'

    try:
        rank_kd = str(int(
            original_stats['seasonalStats']['kills'] /
            original_stats['seasonalStats']['deaths'] * 100) / 100)
    except ZeroDivisionError:
        rank_kd = 0

    try:
        rank_win_rate = str(int(original_stats['seasonalStats']['wins'] /
                                (original_stats['seasonalStats']['wins'] + original_stats['seasonalStats']['losses'])
                                * 10000) / 100) + '%'
    except ZeroDivisionError:
        rank_win_rate = '00.00%'

    stats = {
        'username': original_stats['username'],
        'uuid': original_stats['ubisoft_id'],
        'avatar_url': original_stats['avatar_url_256'],
        'last_updated': original_stats['last_updated'],
        'level': original_stats['progressionStats']['level'],
        'general': {
            'kd': general_kd,
            'win_rate': general_win_rate,
            'kills_per_game': general_win_kills_per_game,
            'kills': original_stats['genericStats']['general']['kills'],
            'wins': original_stats['genericStats']['general']['wins'],
            'games_played': original_stats['genericStats']['general']['games_played'],
            'deaths': original_stats['genericStats']['general']['deaths'],
            'losses': original_stats['genericStats']['general']['losses'],
            'playtime': general_playtime,
            'dbnos': original_stats['genericStats']['general']['dbnos'],
            'rank_kd': general_rank_kd,
            'casual_kd': general_casual_kd,
        },
        'multi': {
            'kills': original_stats['genericStats']['general']['kills'],
            'blind_kills': original_stats['genericStats']['general']['blind_kills'],
            'melee_kills': original_stats['genericStats']['general']['melee_kills'],
            'penetration_kills': original_stats['genericStats']['general']['penetration_kills'],
            'headshots': original_stats['genericStats']['general']['headshots'],
            'headshots_rate': multi_headshots_rate,
            'assists': original_stats['genericStats']['general']['assists'],
            'revives': original_stats['genericStats']['general']['revives'],
            'suicides': original_stats['genericStats']['general']['suicides'],
            'barricades_deployed': original_stats['genericStats']['general']['barricades_deployed'],
            'reinforcements_deployed': original_stats['genericStats']['general']['reinforcements_deployed'],
            'rappel_breaches': original_stats['genericStats']['general']['rappel_breaches'],
        },
        'rank': {
            'MMR': original_stats['seasonalStats']['mmr'],
            'max_MMR': original_stats['seasonalStats']['max_mmr'],
            'wins': original_stats['seasonalStats']['wins'],
            'losses': original_stats['seasonalStats']['losses'],
            'kills': original_stats['seasonalStats']['kills'],
            'deaths': original_stats['seasonalStats']['deaths'],
            'kd': rank_kd,
            'win_rate': rank_win_rate,
            'region': original_stats['seasonalStats']['region'],
            'rank': rank(original_stats['seasonalStats']['max_mmr']),
        },
    }
    return stats


def rank(mmr: int):
    if mmr == 0:
        return {'name': '未排名', 'id': 'Unranked'}

    elif mmr < 1200:
        return {'name': '紫铜 V', 'id': 'Copper_05'}
    elif 1200 <= mmr <= 1299:
        return {'name': '紫铜 IV', 'id': 'Copper_04'}
    elif 1300 <= mmr <= 1399:
        return {'name': '紫铜 III', 'id': 'Copper_03'}
    elif 1400 <= mmr <= 1499:
        return {'name': '紫铜 II', 'id': 'Copper_02'}
    elif 1500 <= mmr <= 1599:
        return {'name': '紫铜 I', 'id': 'Copper_01'}

    elif 1600 <= mmr <= 1699:
        return {'name': '青铜 V', 'id': 'Bronze_05'}
    elif 1700 <= mmr <= 1799:
        return {'name': '青铜 IV', 'id': 'Bronze_04'}
    elif 1800 <= mmr <= 1899:
        return {'name': '青铜 III', 'id': 'Bronze_03'}
    elif 1900 <= mmr <= 1999:
        return {'name': '青铜 II', 'id': 'Bronze_02'}
    elif 2000 <= mmr <= 2099:
        return {'name': '青铜 I', 'id': 'Bronze_01'}

    elif 2100 <= mmr <= 2199:
        return {'name': '白银 V', 'id': 'Silver_05'}
    elif 2200 <= mmr <= 2299:
        return {'name': '白银 IV', 'id': 'Silver_04'}
    elif 2300 <= mmr <= 2399:
        return {'name': '白银 III', 'id': 'Silver_03'}
    elif 2400 <= mmr <= 2499:
        return {'name': '白银 II', 'id': 'Silver_02'}
    elif 2500 <= mmr <= 2599:
        return {'name': '白银 I', 'id': 'Silver_01'}

    elif 2600 <= mmr <= 2799:
        return {'name': '黄金 III', 'id': 'Gold_03'}
    elif 2800 <= mmr <= 2999:
        return {'name': '黄金 II', 'id': 'Gold_02'}
    elif 3000 <= mmr <= 3199:
        return {'name': '黄金 I', 'id': 'Gold_01'}

    elif 3200 <= mmr <= 3599:
        return {'name': '白金 III', 'id': 'Platinum_03'}
    elif 3600 <= mmr <= 3999:
        return {'name': '白金 II', 'id': 'Platinum_02'}
    elif 4000 <= mmr <= 4399:
        return {'name': '白金 I', 'id': 'Platinum_01'}

    elif 4400 <= mmr <= 4999:
        return {'name': '钻石', 'id': 'Diamond_01'}

    elif 5000 <= mmr:
        return {'name': '冠军', 'id': 'Champions_01'}


if __name__ == '__main__':
    async def test():
        print(await get_stats('CN.Eternity'))

    import asyncio

    asyncio.run(test())
