import random
from .OrbofTrnsmutation import Orb_of_Transmutation
from .OrbofAlchemy import Orb_of_Alchemy

def Orb_of_Chance(iteminfo):
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] != 'normal':
        reward = -10
        return iteminfo, reward

    rd = random.choices(population=['normal', 'magic', 'rare'],
                        weights=[6, 3, 1])

    if rd == 'normal':
        iteminfo, reward = iteminfo, reward

    elif rd == 'magic':
       iteminfo, reward = Orb_of_Transmutation(iteminfo)

    elif rd == 'rare':
        iteminfo, reward = Orb_of_Alchemy(iteminfo)

    return iteminfo, reward