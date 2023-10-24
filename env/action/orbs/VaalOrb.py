import json
import random as rd
from .OrbofAlchemy import Orb_of_Alchemy
from .ChaosOrb import Chaos_Orb
from .OrbofScouring import Orb_of_Scouring

"""
result of vaal orb

1. None (But item corrupted)
2. To rare (item base maintained)
3. vaal option

98. to unique <- one of fail
99. related to socket <- never mind

weight
1) start from normal
(1 + 98 + 99 : 2 : 3) = : 1/4 : 1/10
2) start from magic
(1 + 98 + 99 : 2 : 3) = : 1/4 : 1/10
3) start from rare
(1 + 98 + 99 : 2 : 3) = : 1/4 : 1/10

"""

def Vaal_Orb(iteminfo):
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    r = rd.choices(population=['none', 'to_rare', 'add_vaal_mod'], weights=[13/20, 1/4, 1/10])[0]

    if r == 'to_rare':
        if iteminfo['rarity'] == 'normal':
            iteminfo, reward = Orb_of_Alchemy(iteminfo)

        if iteminfo['rarity'] == 'magic':
            iteminfo, reward = Orb_of_Scouring(iteminfo)
            iteminfo, reward = Orb_of_Alchemy(iteminfo)

        if iteminfo['rarity'] == 'rare':
            iteminfo, reward = Chaos_Orb(iteminfo)

        iteminfo['rarity'] = 'rare'

    elif r == 'add_vaal_mod':
        vaal_file_path = 'env/src/json/vaal_mods.json'

        with open(vaal_file_path) as ff:
            vaal_mod_dict = json.load(ff)

        r = rd.choice(list(vaal_mod_dict[iteminfo['base']].keys()))

        r_g = vaal_mod_dict[iteminfo['base']][r]['groups']
        r_i = vaal_mod_dict[iteminfo['base']][r]['implicit_tags']

        head = {'implicit': r, 'groups': r_g, 'implicit_tags': r_i}

        iteminfo['head_implicit'] = head

    iteminfo['status']['corrupted'] = True

    return iteminfo, reward